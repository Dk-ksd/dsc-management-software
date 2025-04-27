from django.db import models
from django.conf import settings 
from datetime import timedelta, date
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db.models import Q
from django.core.exceptions import ValidationError
# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('general-user', 'General User'),
        ('approver', 'Approver'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='general-user')

    def __str__(self):
        return f"{self.username} ({self.role})"
    





class DSC_class(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=150, unique=True)
    
    def __str__(self):
        return self.class_name


class Platform(models.Model):
    platform_id = models.AutoField(primary_key=True)
    platform_name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.platform_name


class IssuingAuth(models.Model):
    auth_id = models.AutoField(primary_key=True)
    auth_name = models.CharField(max_length=100,  unique=True)


    def __str__(self):
        return self.auth_name
    

class Entity(models.Model):
    entity_id = models.AutoField(primary_key=True)
    entity_name = models.CharField(max_length=50, unique=True)


    def __str__(self):
        return self.entity_name    
    

class LicensePeriod(models.Model):
    license_id = models.AutoField(primary_key=True)
    no_of_years = models.IntegerField(unique=True)


    def __str__(self):
        return f"{self.no_of_years} years"   
    

class Forms(models.Model):
    form_id = models.AutoField(primary_key=True)
    form_name = models.CharField(max_length=50,unique=True)


    def __str__(self):
        return self.form_name
    

class Type(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50, unique=True)


    def __str__(self):
        return self.type_name    


class Roles(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.role_name
    

# class Usr(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     user_name = models.CharField(max_length=50, unique=True)
#     role_name = models.ForeignKey(Roles, on_delete=models.CASCADE)
#     def __str__(self):
#         return f"{self.user_name} - {self.role_name} years"
    

class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.status_name    
    

class Shelf(models.Model):
    shelf_id = models.AutoField(primary_key=True)
    shelf_no = models.CharField(max_length=50, unique=True)


    def __str__(self):
        return self.shelf_no    



class DSCMaster(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Expired', 'Expired'),
    ]

    dsc_id = models.AutoField(primary_key=True, serialize=False)
    dsc_type = models.ForeignKey(Type, on_delete=models.CASCADE)
    dsc_number = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100)
    issued_date = models.DateField()
    license_period = models.ForeignKey(LicensePeriod, on_delete=models.CASCADE)
    expiry_date = models.DateField(blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    pan_no = models.CharField(max_length=10, blank=True, null=True )
    dsc_class = models.ForeignKey(DSC_class, on_delete=models.CASCADE, blank=True, null=True)
    email_id = models.EmailField(blank=True, null=True)
    phone_no = models.CharField(max_length=10, blank=True, null=True)
    issuing_auth = models.ForeignKey(IssuingAuth, on_delete=models.CASCADE, blank=True, null=True)
    ref_name = models.CharField(max_length=100, blank=True, null=True)
    ref_contact = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=50, choices=[('Organization', 'Organization'), ('Individual', 'Individual')], blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Active')
    remarks = models.TextField(blank=True, null=True)  # Add this line
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True) 

        # **NEW:** Store additional fields in JSON format
    extra_fields = models.JSONField(default=dict, blank=True)
    
    def save(self, *args, **kwargs):              
        # Auto-calculate expiry date
        if self.issued_date and self.license_period:
            self.expiry_date = self.issued_date + timedelta(days=self.license_period.no_of_years * 365)

        # Auto-update status based on expiry date
        if self.expiry_date:
            self.status = 'Expired' if self.expiry_date < date.today() else 'Active'


        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.dsc_number} - {self.full_name}"




class DSCEntity(models.Model):
    dsc_number = models.ForeignKey(DSCMaster, on_delete=models.CASCADE, related_name="dscentity_set")
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('dsc_number', 'entity')  # Prevent duplicate mappings

    def __str__(self):
        return f"{self.dsc_number} - {self.entity}"



class Docs(models.Model):
    docs_id = models.AutoField(primary_key=True)
    dsc_number = models.ForeignKey('DSCMaster', on_delete=models.CASCADE, related_name='documents')
    aadhar_path = models.FileField(
        upload_to='aadhar-files',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpeg', 'jpg', 'png'])]
    )
    pan_path = models.FileField(
        upload_to='pan-files',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpeg', 'jpg', 'png'])]
    )
    pp_path = models.FileField(
        upload_to='pp-files',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpeg', 'jpg', 'png'])]
    )

    def __str__(self):
        return f"{self.dsc_number.dsc_number} Documents"


class InOut(models.Model):
    Direction_Choices = [
        ('in', 'in'),  
        ('out', 'out')  
    ]

    in_out_id = models.AutoField(primary_key=True)
    dsc_number = models.ForeignKey(DSCMaster, to_field='dsc_number', on_delete=models.CASCADE)
    direction = models.CharField(max_length=10, choices=Direction_Choices, default='in')  # ✅ Default is IN

    # Initiation Fields
    initiated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="initiations", null=True, blank=True)
    initiation_date = models.DateTimeField(auto_now_add=True)
    requester_name = models.CharField(max_length=100)
    initiation_remarks = models.TextField(blank=True, null=True)
    initiated = models.BooleanField(default=False)  # ✅ Tracks initiation status

    # Delivery/Collection Fields
    action_date = models.DateField(null=True, blank=True)
    action_time = models.TimeField(null=True, blank=True)
    agent_name = models.CharField(max_length=100, blank=True, null=True)
    agent_mob = models.CharField(max_length=15, blank=True, null=True)
    action_remarks = models.TextField(blank=True, null=True)
    action_completed = models.BooleanField(default=False)  # ✅ Tracks completion status

    def save(self, *args, **kwargs):
        # ✅ Only change direction if this is NOT a newly created DSC
        if self.action_completed and self.initiated_by is not None:  
            if self.direction == 'in':  
                self.direction = 'out'  # ✅ Change to OUT when delivered
            else:  
                self.direction = 'in'  # ✅ Change to IN when collected

        super(InOut, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.dsc_number} ({self.direction}) - Initiated: {self.initiated}, Completed: {self.action_completed}"





class DSCRenewal(models.Model):
    additional_id = models.AutoField(primary_key=True)  # Unique identifier for the renewal entry
    dsc_number = models.ForeignKey('DSCMaster', on_delete=models.CASCADE, related_name="renewals")
  # Link to DSCMaster
    shelf_no = models.ForeignKey(Shelf, on_delete=models.SET_NULL, null=True, blank=True)  # Select shelf number
    gst_reg_date = models.DateField(blank=True, null=True)
    it_reg_date = models.DateField(blank=True, null=True)
    mca_reg_date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Renewal Details for {self.dsc_number.dsc_number}"


class UsageLogs(models.Model):
    log_id = models.AutoField(primary_key=True)
    dsc_id = models.ForeignKey(DSCMaster, on_delete=models.CASCADE)  # ✅ Use `dsc_id`
    form_id = models.ForeignKey(Forms, on_delete=models.SET_NULL, null=True, blank=True)
    form_other = models.CharField(max_length=50, blank=True, null=True)
    platform_id = models.ForeignKey(Platform,on_delete=models.SET_NULL, null=True, blank=True)
    platform_other = models.CharField(max_length=50, blank=True, null=True)
    date_of_usage = models.DateField()

    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="requests")  
    approved_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    approval_status = models.CharField(max_length=10, choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")], default="pending")

    def __str__(self):
        return f"Usage Log: {self.log_id} - DSC ID: {self.dsc_id}"

    @property
    def form_name(self):
        return self.form_other if self.form_other else (self.form_id.form_name if self.form_id else "N/A")
    
    @property
    def platform_name(self):
        return self.platform_other if self.platform_other else (self.platform_id.platform_name if self.platform_id else "N/A")

    class Meta:
        db_table = "usage_logs"


class DSCExtraField(models.Model):
    DSC_TYPE_CHOICES = [
        ('internal', 'Internal'),
        ('external', 'External'),
        ('both', 'Both'),
    ]
    
    FIELD_TYPE_CHOICES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('boolean', 'Boolean'),
    ]
    
    dsc_type = models.CharField(max_length=20, choices=DSC_TYPE_CHOICES)
    field_name = models.CharField(max_length=100, unique=True)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPE_CHOICES)
    required = models.BooleanField(default=False)
    label = models.CharField(max_length=100, blank=True, null=True)

    def clean(self):
        # Ensure field_name is valid Python/Django identifier
        if not self.field_name.isidentifier():
            raise ValidationError("Field name must be a valid Python identifier (letters, numbers, underscores)")
    
    def __str__(self):
        return f"{self.get_dsc_type_display()}: {self.label or self.field_name}"

class DSCExtraData(models.Model):
    dsc_number = models.ForeignKey(DSCMaster, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    value = models.TextField()

    class Meta:
        unique_together = ('dsc_number', 'field_name')
    def __str__(self):
        return f"{self.dsc_number} - {self.field_name}: {self.value}"



class EmailTemplate(models.Model):
    TEMPLATE_TYPES = [
        ('expired', 'Expired DSC Notification'),
        ('expiring', 'Expiring Soon DSC Notification'),
    ]
    
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES, unique=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_template_type_display()