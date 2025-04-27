from datetime import date, timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import DSCMaster, EmailTemplate

def send_dsc_expiry_notifications(notification_type=None):

    print(f"Notification type received: {notification_type}") 
    today = date.today()
    
    try:
        if notification_type == 'expired' or notification_type is None:
            expired_template = EmailTemplate.objects.get(template_type='expired')
            expired_dscs = DSCMaster.objects.filter(
                expiry_date__lt=today,
                status="Expired"
            )
            for dsc in expired_dscs:
                if dsc.email_id:
                    send_mail(
                        expired_template.subject.format(
                            dsc_number=dsc.dsc_number,
                            full_name=dsc.full_name,
                            expiry_date=dsc.expiry_date
                        ),
                        expired_template.body.format(
                            dsc_number=dsc.dsc_number,
                            full_name=dsc.full_name,
                            expiry_date=dsc.expiry_date
                        ),
                        settings.DEFAULT_FROM_EMAIL,
                        [dsc.email_id],
                        fail_silently=False
                    )
        
        if notification_type == 'expiring' or notification_type is None:
            expiring_template = EmailTemplate.objects.get(template_type='expiring')
            expiring_dscs = DSCMaster.objects.filter(
                expiry_date__gte=today,
                expiry_date__lte=today + timedelta(days=30),
                status="Active"
            )
            for dsc in expiring_dscs:
                if dsc.email_id:
                    send_mail(
                        expiring_template.subject.format(
                            dsc_number=dsc.dsc_number,
                            full_name=dsc.full_name,
                            expiry_date=dsc.expiry_date
                        ),
                        expiring_template.body.format(
                            dsc_number=dsc.dsc_number,
                            full_name=dsc.full_name,
                            expiry_date=dsc.expiry_date
                        ),
                        settings.DEFAULT_FROM_EMAIL,
                        [dsc.email_id],
                        fail_silently=False
                    )
                    
    except EmailTemplate.DoesNotExist:
        # Fallback to original behavior if templates not configured
        pass