from django import forms
from .models import DSC_class,Platform,IssuingAuth, Entity, LicensePeriod, Forms, Type, Status, DSCMaster, InOut, Docs, Shelf, DSCRenewal,UsageLogs, DSCEntity, CustomUser, DSCExtraField,DSCExtraData,EmailTemplate,ShelfAssignment,RenewalExtraField
from django.shortcuts import render, get_object_or_404
import re
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from datetime import date
from django.utils.timezone import now
from .models import DSCMaster, DSCExtraField, Type
from django.db.models import Q

class DateInput(forms.DateInput):
    input_type='date'

class ClassForm(forms.ModelForm):
    class Meta:
        model = DSC_class
        fields = '__all__'

        widgets = {
            'class_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def clean(self): ##############
            cleaned_data = super().clean()
            class_name = cleaned_data.get('class_name')

            # Check for duplicates only if not already raised
            if DSC_class.objects.filter(class_name=class_name).exists():
                self.add_error('class_name', "A class with this name already exists.")
        
            return cleaned_data

class PlatformForm(forms.ModelForm):
    class Meta:
        model = Platform
        fields = '__all__'

        widgets = {
            'platform_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def clean(self): ##############
            cleaned_data = super().clean()
            class_name = cleaned_data.get('platform_name')

            # Check for duplicates only if not already raised
            if Platform.objects.filter(platform_name='platform_name').exists(): ###PRBLM
                self.add_error('auth_name', "A Platform with this name already exists.")
        
            return cleaned_data


class IssuingAuthForm(forms.ModelForm):
    class Meta:
        model = IssuingAuth
        fields = '__all__'
        
        widgets = {
            'auth_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'auth_name' : 'Authority Name',
        }

        def clean(self): ##############
            cleaned_data = super().clean()
            auth_name = cleaned_data.get('auth_name')

            # Check for duplicates only if not already raised
            if IssuingAuth.objects.filter(auth_name='auth_name').exists():
                self.add_error('auth_name', "A entity with this name already exists.")
        
            return cleaned_data
        

class EntityForm(forms.ModelForm):
    class Meta:
        model = Entity
        fields = '__all__'

        widgets = {
            'entity_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def clean(self): ##############
            cleaned_data = super().clean()
            entity_name = cleaned_data.get('entity_name')

            # Check for duplicates only if not already raised
            if Entity.objects.filter(entity_name=entity_name).exists():
                self.add_error('entity_name', "A entity with this name already exists.")
        
            return cleaned_data        
        

class LicenseForm(forms.ModelForm):
    class Meta:
        model = LicensePeriod
        fields = '__all__'

        widgets = {
            'no_of_years': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'no_of_years' : 'Period of License',
        }

        def clean(self): ##############
            cleaned_data = super().clean()
            no_of_years = cleaned_data.get('no_of_years')

            # Check for duplicates only if not already raised
            if LicensePeriod.objects.filter(no_of_years=no_of_years).exists():
                self.add_error('no_of_years', "Already exists.")
        
            return cleaned_data
        

class FormsForm(forms.ModelForm):
    class Meta:
        model = Forms
        fields = '__all__'

        widgets = {
            'form_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def clean(self): ##############
            cleaned_data = super().clean()
            form_name = cleaned_data.get('form_name')

            # Check for duplicates only if not already raised
            if Forms.objects.filter(form_name=form_name).exists():
                self.add_error('form_name', "Already exists.")
        
            return cleaned_data
        

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = '__all__'

        widgets = {
            'type_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def clean(self): ##############
            cleaned_data = super().clean()
            type_name = cleaned_data.get('type_name')

            # Check for duplicates only if not already raised
            if Type.objects.filter(type_name=type_name).exists():
                self.add_error('type_name', "A Type with this name already exists.")
        
            return cleaned_data        
        

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'      

        def clean(self): ##############
            cleaned_data = super().clean()
            status_name = cleaned_data.get('status_name')

            # Check for duplicates only if not already raised
            if Status.objects.filter(status_name='status_name').exists(): ###PRBLM
                self.add_error('status_name', "already exists.")
        
            return cleaned_data  


class ShelfForm(forms.ModelForm):
    class Meta:
        model = Shelf
        fields = '__all__'

        widgets = {
            'shelf_no': forms.TextInput(attrs={'class': 'form-control'}),
        }


        def clean(self): ##############
            cleaned_data = super().clean()
            shelf_no = cleaned_data.get('shelf_no')

            # Check for duplicates only if not already raised
            if Shelf.objects.filter(shelf_no=shelf_no).exists():
                self.add_error('shelf_no', "Shelf number already exists.")
        
            return cleaned_data



class InternalDSCForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get last internal DSC entry and increment number
        try:
            # Filter by internal type
            internal_type = Type.objects.get(type_name='Internal')
            last_internal_dsc = DSCMaster.objects.filter(dsc_type=internal_type).order_by('-dsc_id').first()
            
            if last_internal_dsc and last_internal_dsc.dsc_number:
                # Extract numeric part if the format is like "INT-001"
                if '-' in last_internal_dsc.dsc_number:
                    prefix, number = last_internal_dsc.dsc_number.split('-')
                    new_number = int(number) + 1
                    next_dsc_number = f"{prefix}-{new_number:03d}"
                else:
                    # If it's just a number, increment it
                    next_dsc_number = str(int(last_internal_dsc.dsc_number) + 1)
            else:
                # First entry
                next_dsc_number = "INT-001"
                
            # Set initial value and make field readonly
            self.fields['dsc_number'].initial = next_dsc_number
            self.fields['dsc_number'].widget.attrs['readonly'] = True
            
        except (Type.DoesNotExist, ValueError):
            # Handle exceptions
            pass

        # Cache extra fields for performance
        self.extra_fields = DSCExtraField.objects.filter(
            Q(dsc_type='internal') | Q(dsc_type='both')
        ).order_by('field_name')

        #Load existing extra data when editing
        # if self.instance and self.instance.pk:
        #     for data in DSCExtraData.objects.filter(dsc_number=self.instance):
        #         self.initial[data.field_name] = data.value

        # Add dynamic fields
        for field in self.extra_fields:
            field_args = {
                'required': field.required,
                'label': field.label or field.field_name.replace('_', ' ').title(),
            }

            if field.field_type == "number":
                self.fields[field.field_name] = forms.IntegerField(**field_args)
            elif field.field_type == "date":
                self.fields[field.field_name] = forms.DateField(
                    **field_args,
                    widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
                )
            elif field.field_type == "boolean":
                self.fields[field.field_name] = forms.BooleanField(
                    required=False,  # Important: Boolean fields shouldn't be required
                    widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                    label=field_args['label']
                )
            else:
                self.fields[field.field_name] = forms.CharField(
                    **field_args,
                    widget=forms.TextInput(attrs={'class': 'form-control'})
                )


    class Meta:
        model = DSCMaster
        exclude = ['user_id'] 
        fields = [
            'dsc_number', 'full_name', 'issued_date', 'license_period', 
            'password', 'pan_no', 'dsc_class', 'email_id', 'phone_no', 'issuing_auth',
            'ref_name', 'ref_contact', 'type', 'remarks'
        ]
        widgets = {
            'dsc_number': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'issued_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'license_period': forms.Select(attrs={'class': 'form-select'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'pan_no': forms.TextInput(attrs={'class': 'form-control'}),
            'dsc_class': forms.Select(attrs={'class': 'form-select'}),
            'email_id': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'issuing_auth': forms.Select(attrs={'class': 'form-select'}),
            'ref_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ref_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
        }

        labels = {
            'dsc_number': mark_safe('DSC Number <span class="text-danger">*</span>'),
            'full_name': mark_safe('Full Name <span class="text-danger">*</span>'),
            'issued_date': mark_safe('Date of Issuing <span class="text-danger">*</span>'),
            'license_period': mark_safe('Period of License <span class="text-danger">*</span>'),
            'password': mark_safe('Password <span class="text-danger">*</span>'),
            'pan_no': mark_safe('PAN <span class="text-danger">*</span>'),
            'dsc_class': mark_safe('Class of DSC <span class="text-danger">*</span>'),
            'email_id': mark_safe('Email ID <span class="text-danger">*</span>'),
            'phone_no': mark_safe('Phone No. <span class="text-danger">*</span>'),
            'issuing_auth': mark_safe('Issuing Authority <span class="text-danger">*</span>'),
            'ref_name': mark_safe('Reference Person <span class="text-danger">*</span>'),
            'ref_contact': mark_safe('Reference Contact <span class="text-danger">*</span>'),
            'type': mark_safe('Type <span class="text-danger">*</span>'),
            'remarks': mark_safe('Remarks <span class="text-danger">*</span>'),
        }


    # ✅ **Phone Number Validation (10 Digits Only)**
    def clean_phone_no(self):
        phone = self.cleaned_data.get('phone_no')
        if not phone:  
            raise ValidationError("❌ Phone No. is required.")
        if phone:
            if not re.match(r'^\d{10}$', phone):
                raise ValidationError("❌ Phone number must be exactly 10 digits.")
        return phone


    # ✅ **Email Validation**
    def clean_email_id(self):
        email = self.cleaned_data.get('email_id')
        if not email:  
            raise ValidationError("❌ Email is required.")
        if email:
            email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_pattern, email):
                raise ValidationError("❌ Invalid email format.")
        return email

    # ✅ **PAN Validation**
    def clean_pan_no(self):
        pan_no = self.cleaned_data.get('pan_no')
        if not pan_no:  
            raise ValidationError("❌ PAN No. is required.")
        if pan_no:
            pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'

            if not re.match(pan_pattern, pan_no):
                raise ValidationError("❌ Invalid PAN format. Expected format: ABCDE1234F.")

            # ✅ Check for duplicate PAN numbers
            existing_pan = DSCMaster.objects.filter(pan_no=pan_no).exclude(pk=self.instance.pk if self.instance else None)

            if existing_pan.exists():
                raise ValidationError("❌ A DSC with this PAN number already exists. Duplicate PANs are not allowed.")

        return pan_no


    # ✅ **Password Validation**
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:  
            raise ValidationError("❌ Password is required.")
        if password:
            if len(password) < 6:
                raise ValidationError("❌ Password must be at least 6 characters long.")
            if not any(char.isdigit() for char in password):
                raise ValidationError("❌ Password must contain at least one number.")
            if not any(char.isalpha() for char in password):
                raise ValidationError("❌ Password must contain at least one letter.")
            if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/~`" for char in password):
                raise ValidationError("❌ Password must contain at least one special character.")
        return password


    # ✅ **Issued Date Validation**
    def clean_issued_date(self):
        issued_date = self.cleaned_data.get('issued_date')
        if issued_date and issued_date > now().date():
            raise ValidationError("❌ Issued date cannot be in the future.")
        return issued_date
    
    # ✅ Reference Contact Validation (10 digits only)
    def clean_ref_contact(self):
        ref_contact = self.cleaned_data.get('ref_contact')
        if not ref_contact:  
            raise ValidationError("❌ Reference Contact is required.")
        if ref_contact:
            contact_pattern = r'^\d{10}$'
            if not re.match(contact_pattern, ref_contact):
                raise ValidationError("❌ Reference contact must be exactly 10 digits.")
            
        return ref_contact


    # ✅ Ensures **ALL** Required Fields Are Filled **(ONE SINGLE ERROR)**
    # ✅ General Required Fields Validation
    def clean(self):
        cleaned_data = super().clean()
        required_fields = {
            'dsc_number': "DSC Number",
            'full_name': "Full Name",
            'issued_date': "Date of Issuing",
            'license_period': "Period of License",
            'dsc_class': "Class of DSC",
            
            'issuing_auth': "Issuing Authority",
            'ref_name': "Reference Person",
            
            'type': "Type",
            'remarks': "Remarks",
        }
        for field_name, display_name in required_fields.items():
            if not cleaned_data.get(field_name):
                self.add_error(field_name, f"❌ {display_name} is required.")

                # Check extra fields
        for field in self.extra_fields:
            if field.required and not cleaned_data.get(field.field_name):
                self.add_error(field.field_name, "This field is required")

        missing_fields = [field_name for field, field_name in required_fields.items() if not cleaned_data.get(field)]
       

        if missing_fields:
            raise ValidationError(f"❌ Please fill in all required fields for Internal DSC: {', '.join(missing_fields)}.")

        return cleaned_data





class ExternalDSCForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Auto-generate external DSC number
        try:
            external_type = Type.objects.get(type_name='External')
            last_external_dsc = DSCMaster.objects.filter(dsc_type=external_type).order_by('-dsc_id').first()
            
            if last_external_dsc and last_external_dsc.dsc_number:
                # Extract numeric part if the format is like "E001"
                if last_external_dsc.dsc_number.startswith('E'):
                    try:
                        last_num = int(last_external_dsc.dsc_number[1:])
                        next_dsc_number = f"E{last_num + 1:04d}"  # Format as E0002, E0003, etc.
                    except ValueError:
                        # Fallback if number parsing fails
                        next_dsc_number = "E0001"
                else:
                    next_dsc_number = "E0001"
            else:
                # First external DSC
                next_dsc_number = "E0001"
                
            # Set initial value and make field readonly
            self.fields['dsc_number'].initial = next_dsc_number
            self.fields['dsc_number'].widget.attrs['readonly'] = True
            
        except (Type.DoesNotExist, ValueError):
            # Handle exceptions
            pass

        self.extra_fields = DSCExtraField.objects.filter(
            Q(dsc_type='external') | Q(dsc_type='both')
        ).order_by('field_name')

        # # Load existing data for editing
        # if self.instance and self.instance.pk:
        #     for data in DSCExtraData.objects.filter(dsc_number=self.instance):
        #         self.initial[data.field_name] = data.value

        # Add dynamic fields
        for field in self.extra_fields:
            field_args = {
                'required': field.required,
                'label': field.label or field.field_name.replace('_', ' ').title(),
            }

            if field.field_type == "number":
                self.fields[field.field_name] = forms.IntegerField(**field_args)
            elif field.field_type == "date":
                self.fields[field.field_name] = forms.DateField(
                    **field_args,
                    widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
            elif field.field_type == "boolean":
                self.fields[field.field_name] = forms.BooleanField(
                    required=False,
                    widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                    label=field_args['label']
                )
            else:
                self.fields[field.field_name] = forms.CharField(
                    **field_args,
                    widget=forms.TextInput(attrs={'class': 'form-control'})
                )
    class Meta:
        model = DSCMaster
        exclude = ['user_id'] 
        fields = [
            'dsc_number', 'full_name', 'issued_date', 'license_period', 'password', 'remarks',
            'pan_no', 'dsc_class', 'email_id', 'phone_no', 'issuing_auth',
            'ref_name', 'ref_contact', 'type'  # ✅ Added missing fields
        ]
        widgets = {
            'dsc_number': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'issued_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date',
            'max': now().date().isoformat()   }),
            'license_period': forms.Select(attrs={'class': 'form-select'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'pan_no': forms.TextInput(attrs={'class': 'form-control', 'required': False}),  # Optional
            'dsc_class': forms.Select(attrs={'class': 'form-select', 'required': False}),  # Optional
            'email_id': forms.EmailInput(attrs={'class': 'form-control', 'required': False}),  # Optional
            'phone_no': forms.TextInput(attrs={'class': 'form-control', 'required': False}),  # Optional
            'issuing_auth': forms.Select(attrs={'class': 'form-select', 'required': False}),  # Optional
            'ref_name': forms.TextInput(attrs={'class': 'form-control', 'required': False}),  # Optional
            'ref_contact': forms.TextInput(attrs={'class': 'form-control', 'required': False}),  # Optional
            'type': forms.Select(attrs={'class': 'form-select', 'required': False}),  # Optional
            
        }
        labels = {
            'dsc_number': mark_safe('DSC Number <span class="text-danger">*</span>'),
            'full_name': mark_safe('Full Name <span class="text-danger">*</span>'),
            'issued_date': mark_safe('Date of Issuing <span class="text-danger">*</span>'),
            'license_period': mark_safe('Period of License <span class="text-danger">*</span>'),
            'password': mark_safe('Password <span class="text-danger">*</span>'),
            'remarks': mark_safe('Remarks <span class="text-danger">*</span>'),
        }

    
        # ✅ Password Validation
   
    # ✅ **Password Validation**
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:  
            raise ValidationError("❌ Password is required.")
        # Check if password contains only digits
        # if not password.isdigit():
        #     raise ValidationError("❌ Password must contain numbers only.")
        if len(password) < 6:
            raise ValidationError("❌ Password must be at least 6 characters.")


        return password

        # ✅ PAN Number Validation
    def clean_pan_no(self):
        pan_no = self.cleaned_data.get('pan_no')
        if pan_no:  # PAN is optional but must be valid if provided
            pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'  # ✅ Format: ABCDE1234F
            
            if not re.match(pan_pattern, pan_no):
                raise ValidationError("❌ Invalid PAN format. Expected format: ABCDE1234F.")
            # return pan_no.upper()  # ✅ Ensure it's always stored in uppercase
        
            existing_pan = DSCMaster.objects.filter(pan_no=pan_no).exclude(pk=self.instance.pk if self.instance else None)
            if existing_pan.exists():
                raise ValidationError("❌ A DSC with this PAN number already exists. Duplicate PANs are not allowed.")
        return pan_no
    
    
        # ✅ Phone Number Validation (10 digits only)
    def clean_phone_no(self):
        phone_no = self.cleaned_data.get('phone_no')
        if phone_no:  
            phone_pattern = r'^\d{10}$'  # ✅ Must be 10 digits
            if not re.match(phone_pattern, phone_no):
                raise ValidationError("❌ Phone number must be exactly 10 digits.")
            
            
        return phone_no

    # ✅ Reference Contact Validation (10 digits only)
    def clean_ref_contact(self):
        ref_contact = self.cleaned_data.get('ref_contact')
        if ref_contact:
            contact_pattern = r'^\d{10}$'
            if not re.match(contact_pattern, ref_contact):
                raise ValidationError("❌ Reference contact must be exactly 10 digits.")
            
        return ref_contact
    
    def clean_issued_date(self):
        issued_date = self.cleaned_data.get('issued_date')
        if issued_date and issued_date > now().date():
            raise ValidationError("❌ Issued date cannot be in the future.")
        return issued_date
    
    def clean_remarks(self):
        remarks = self.cleaned_data.get('remarks')
        if not remarks:  
            raise ValidationError("❌ Remarks is required.")
        return remarks
        
    def clean(self):
        cleaned_data = super().clean()
        required_fields = ['dsc_number', 'full_name', 'issued_date', 'license_period']

        # Check extra fields
        for field in self.extra_fields:
            if field.required and not cleaned_data.get(field.field_name):
                self.add_error(field.field_name, "This field is required")

        # ✅ Check if any required field is missing
        missing_fields = [field for field in required_fields if not cleaned_data.get(field)]
        if missing_fields:
            raise forms.ValidationError(f"❌ Please fill in all required fields for External DSC.")
        
        return 





class DocsForm(forms.ModelForm):
    class Meta:
        model = Docs
        fields = ['aadhar_path', 'pan_path', 'pp_path']
        widgets = {
            'aadhar_path': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*,application/pdf'}),
            'pan_path': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*,application/pdf'}),
            'pp_path': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*,application/pdf'}),
        }

    def __init__(self, *args, **kwargs):
        dsc_type = kwargs.pop('dsc_type', None)  # ✅ Get DSC Type (Internal/External)
        is_renewal = kwargs.pop('is_renewal', False)  # ✅ Check if form is for renewal
        super(DocsForm, self).__init__(*args, **kwargs)

        if dsc_type and dsc_type.lower() == 'internal':
            # ✅ Make fields required and add red star (*) for Internal DSC
            self.fields['aadhar_path'].required = True
            self.fields['pan_path'].required = True
            self.fields['pp_path'].required = True

            self.fields['aadhar_path'].label = mark_safe('Aadhar Document <span class="text-danger">*</span>')
            self.fields['pan_path'].label = mark_safe('PAN Document <span class="text-danger">*</span>')
            self.fields['pp_path'].label = mark_safe('PP Photo <span class="text-danger">*</span>')
        else:
            # ✅ Make fields optional and remove red star for External DSC
            self.fields['aadhar_path'].required = False
            self.fields['pan_path'].required = False
            self.fields['pp_path'].required = False

            self.fields['aadhar_path'].label = 'Aadhar Document'
            self.fields['pan_path'].label = 'PAN Document'
            self.fields['pp_path'].label = 'PP Photo'

    def clean(self):
        # ✅ Prevent accidental document removal by keeping existing files if no new ones are uploaded. """
        cleaned_data = super().clean()

        if self.instance:  # ✅ If editing an existing document entry
            if not cleaned_data.get('aadhar_path'):
                cleaned_data['aadhar_path'] = self.instance.aadhar_path
            if not cleaned_data.get('pan_path'):
                cleaned_data['pan_path'] = self.instance.pan_path
            if not cleaned_data.get('pp_path'):
                cleaned_data['pp_path'] = self.instance.pp_path

        return cleaned_data



class DSCEntityForm(forms.ModelForm):
    dsc_number = forms.ModelChoiceField(
        queryset=DSCMaster.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    entity = forms.ModelChoiceField(
        queryset=Entity.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )

    class Meta:
        model = DSCEntity
        fields = ['dsc_number', 'entity']






class InOutForm(forms.ModelForm):
   
    class Meta:
        model = InOut
        fields = '__all__'

        widgets = {
            'initiation_date' : forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'action_date' :  forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'direction': forms.Select(attrs={'class': 'form-select'}),
            "dsc_number": forms.Select(attrs={"class": "form-select select2"}),
            "requester_name": forms.TextInput(attrs={"class": "form-control"}),
            "initiation_remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            'agent_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'agent_mob' : forms.TextInput(attrs={'class': 'form-control'}),
            'action_remarks' : forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['direction'].initial = 'outgoing'  # Set default to "Outgoing"

       
 




from .forms import DateInput  # Assuming DateInput is already defined in your forms



class UsageLogsForm(forms.ModelForm):
    form_other = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={"placeholder": "Enter new form name"})
    )
    platform_other = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={"placeholder": "Enter new platform name"})
    )

    class Meta:
        model = UsageLogs
        exclude = ['approved_by_user', 'approval_status', 'requested_by']

        widgets = {
            'date_of_usage': DateInput,
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)  # ✅ Get request object
        super().__init__(*args, **kwargs)

        # ✅ Dynamically add "Other" option to form and platform choices
        self.fields['form_id'].queryset = Forms.objects.all()
        self.fields['form_id'].choices = list(self.fields['form_id'].choices) + [("other", "Other")]

        self.fields['platform_id'].queryset = Platform.objects.all()
        self.fields['platform_id'].choices = list(self.fields['platform_id'].choices) + [("other", "Other")]

    def save(self, commit=True):
        instance = super().save(commit=False)

        # ✅ Automatically set requested_by as the logged-in user
        if self.request and self.request.user.is_authenticated:
            instance.requested_by = self.request.user  

        if commit:
            instance.save()
        return instance




from django.contrib.auth import get_user_model
User = get_user_model()




class UserForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }

class EditUserForm(forms.ModelForm):
    """Form for editing user details with an optional password update."""
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    password = forms.CharField(
        required=False,  # ✅ Optional password change
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Leave blank to keep current password'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

    def save(self, commit=True):
        """Override save method to update password only if provided."""
        user = super().save(commit=False)
        if self.cleaned_data["password"]:
            user.set_password(self.cleaned_data["password"])  # ✅ Hash new password if provided
        if commit:
            user.save()
        return user



class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    

# class LoginForm(forms.Form):
#     username = forms.CharField(
#         max_length=150,
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
#     )

class InitiationForm(forms.ModelForm):
    """Form for DSC Initiation"""
    DIRECTION_CHOICES = [
        ('in', 'Incoming'),
        ('out', 'Outgoing'),
    ]

    direction = forms.ChoiceField(choices=DIRECTION_CHOICES, required=True, widget=forms.RadioSelect)
    requester_name = forms.CharField(label="Name of the Person Requesting DSC", required=False)
    initiation_remarks = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)
    requester_type_value = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = InOut
        fields = ['direction', 'dsc_number', 'requester_name', 'initiation_remarks', 'requester_type_value']
        widgets = {
            'initiation_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def clean(self):
        cleaned_data = super().clean()
        requester_type_value = cleaned_data.get('requester_type_value')
        requester_name = cleaned_data.get('requester_name')

        if requester_type_value == 'other' and not requester_name:
            self.add_error('requester_name', 'This field is required when "Other" is selected.')

        return cleaned_data


class DeliveryCollectionForm(forms.ModelForm):
    class Meta:
        model = InOut
        fields = ['agent_name', 'agent_mob', 'action_date', 'action_time', 'action_remarks']
        widgets = {
            "agent_name": forms.TextInput(attrs={"class": "form-control"}),
            "agent_mob": forms.TextInput(attrs={"class": "form-control"}),
            "action_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "action_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "action_remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }




class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ['subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={"class": "form-control" }),
            'body': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }
        help_texts = {
            'body': 'Available variables: {full_name}, {dsc_number}, {expiry_date}'
        }


class AssignShelfForm(forms.ModelForm):
    class Meta:
        model = ShelfAssignment
        fields = ['shelf_no', 'remarks']
        widgets = {
            'shelf_no': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'shelf_no': 'Shelf Number',
            'remarks': 'Assignment Remarks',
        }

class UnassignShelfForm(forms.ModelForm):
    class Meta:
        model = ShelfAssignment
        fields = ['remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter reason for unassigning this shelf...'
            })
        }

class BulkDSCUploadForm(forms.Form):
    DSC_TYPE_CHOICES = [
        ('internal', 'Internal'),
        ('external', 'External'),
    ]
    
    dsc_type = forms.ChoiceField(
        choices=DSC_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    upload_file = forms.FileField(
        label='Select CSV/Excel file',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv,.xlsx,.xls'})
    )
    
    def clean_upload_file(self):
        file = self.cleaned_data.get('upload_file')
        if file:
            ext = file.name.split('.')[-1].lower()
            if ext not in ['csv', 'xlsx', 'xls']:
                raise ValidationError("Only CSV or Excel files are allowed.")
        return file
    

class DSCRenewalForm(forms.ModelForm):
    class Meta:
        model = DSCRenewal
        fields = ['gst_reg_date', 'it_reg_date', 'mca_reg_date', 'remarks']
        widgets = {
            'it_reg_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'mca_reg_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add dynamic fields from RenewalExtraField
        for field in RenewalExtraField.objects.all().order_by('field_name'):
            field_args = {
                'required': field.required,
                'label': field.label or field.field_name.replace('_', ' ').title(),
                'help_text': field.help_text,
            }

            if field.field_type == "number":
                self.fields[field.field_name] = forms.IntegerField(**field_args)
            elif field.field_type == "date":
                self.fields[field.field_name] = forms.DateField(
                    **field_args,
                    widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
                )
            elif field.field_type == "boolean":
                self.fields[field.field_name] = forms.BooleanField(
                    required=False,
                    widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                    label=field_args['label']
                )
            else:
                self.fields[field.field_name] = forms.CharField(
                    **field_args,
                    widget=forms.TextInput(attrs={'class': 'form-control'})
                )

            # Set initial value if editing
            if self.instance and field.field_name in self.instance.extra_fields:
                self.initial[field.field_name] = self.instance.extra_fields[field.field_name]

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Save extra fields to JSON field
        instance.extra_fields = {}
        for field in RenewalExtraField.objects.all():
            field_name = field.field_name
            if field_name in self.cleaned_data:
                value = self.cleaned_data[field_name]
                if field.field_type == "boolean":
                    value = bool(value)
                instance.extra_fields[field_name] = value
        
        if commit:
            instance.save()
        return instance
    

class BulkEntityUploadForm(forms.Form):
    upload_file = forms.FileField(
        label='Select CSV/Excel file',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv,.xlsx,.xls'})
    )
    
    def clean_upload_file(self):
        file = self.cleaned_data.get('upload_file')
        if file:
            ext = file.name.split('.')[-1].lower()
            if ext not in ['csv', 'xlsx', 'xls']:
                raise ValidationError("Only CSV or Excel files are allowed.")
        return file