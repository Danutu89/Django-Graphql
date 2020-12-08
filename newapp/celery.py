from __future__ import absolute_import
from celery import Celery
import os
import django

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newapp.settings")

app = Celery("newapp", namespace="CELERY_")

django.setup()
from django.conf import settings

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings)


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# Load task modules from all registered Django app configs.


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
