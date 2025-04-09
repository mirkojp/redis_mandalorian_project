from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "redis_mandalorian_project.settings")

app = Celery("redis_mandalorian_project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_url = os.getenv("REDIS_URL")  # este apunta a Upstash
app.autodiscover_tasks()
