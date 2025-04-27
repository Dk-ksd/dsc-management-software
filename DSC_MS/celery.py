# DSC_MS/celery.py
from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DSC_MS.settings')

app = Celery('DSC_MS')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Windows-specific settings
app.conf.broker_connection_retry_on_startup = True
app.conf.broker_url = 'redis://127.0.0.1:6379/0'
app.conf.result_backend = 'redis://127.0.0.1:6379/0'
app.conf.worker_pool = 'solo'

