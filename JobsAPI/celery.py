# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JobsAPI.settings')

app = Celery('JobsAPI')

app.config_from_object(settings, namespace='CELERY')

app.conf.worker_concurrency = 1

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
  print(f'Request: {self.request!r}')

CELERY_CACHE_BACKEND = 'default'
