import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'support_application.settings')

app = Celery('support_application')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
