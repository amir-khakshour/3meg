from __future__ import absolute_import, unicode_literals

import os

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from celery import Celery
from .settings import PROJECT_NAME

app = Celery(PROJECT_NAME)
app.config_from_object(
    'django.conf:settings',
    namespace='CELERY'
)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
