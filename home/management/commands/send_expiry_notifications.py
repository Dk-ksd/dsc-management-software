from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from home.models import DSCMaster
from datetime import timedelta

class Command(BaseCommand):
    help = 'Sends email notifications for expiring/expired DSCs'

    def handle(self, *args, **options):
        today = timezone.now().date()
        expiry_threshold = today + timedelta(days=15)
        
        # Get certificates expiring in 15 days
        expiring_soon = DSCMaster.objects.filter(
            expiry_date__gte=today,
            expiry_date__lte=expiry_threshold,
            status='Active'
        )
        
        # Get expired certificates
        already_expired = DSCMaster.objects.filter(
            expiry_date__lt=today,
            status='Expired'  # Only notify once
        )
        
        # Send notifications
        self.send_notifications(expiring_soon, is_expired=False)
        self.send_notifications(already_expired, is_expired=True)
        
        # Update status for expired certs
        already_expired.update(status='Expired')
        
        self.stdout.write(f"Sent {len(expiring_soon)+len(already_expired)} notifications")

    def send_notifications(self, certificates, is_expired):
        for cert in certificates:
            if not cert.email_id:  # Skip if no email
                continue
                
            subject = "⚠️ Your DSC is Expired!" if is_expired else "🔔 Your DSC Expires Soon!"
            
            message = render_to_string('emails/dsc_expiry_notification.html', {
                'cert': cert,
                'is_expired': is_expired,
                'days_left': (cert.expiry_date - timezone.now().date()).days
            })
            
            send_mail(
                subject,
                message,
                'project41322@gmail.com',  # From email
                [cert.email_id],  # To email
                fail_silently=False,
                html_message=message
            )