from celery.schedules import crontab
from DSC_MS.celery import app

app.conf.beat_schedule = {
    'send-expiry-notifications': {
        'task': 'home.tasks.send_expiry_notifications',
        'schedule': crontab(hour=8, minute=0),  # Runs daily at 8 AM
    },
}