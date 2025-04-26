from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-daily-email-every-morning-7am': {
        'task': 'apps.newsletter.tasks.send_message_newsletter',
        'schedule': crontab(minute='*/3'),
    },
}