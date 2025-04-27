from celery import shared_task
from datetime import date, timedelta
from .models import DSCMaster, EmailTemplate
from .notifications import send_dsc_notification

@shared_task
def check_and_send_dsc_expiry_emails():
    from .notifications import send_dsc_expiry_notifications
    send_dsc_expiry_notifications()