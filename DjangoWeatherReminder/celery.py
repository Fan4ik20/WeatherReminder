import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'DjangoWeatherReminder.settings'
)

app = Celery('DjangoWeatherReminder')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.broker_transport_options = {
    'queue_order_strategy': 'priority',
}

app.conf.beat_schedule = {
    'fill-weather-every-hour': {
        'task': 'django_weather_reminder.tasks.fill_active_cities',
        'schedule': crontab(hour='*', minute='0')
    },
    'send-mail-every-hour': {
        'task': 'django_weather_reminder.tasks.send_mail_every_n_hours',
        'schedule': crontab(hour='*', minute='5'),
        'args': (1,)
    },
    'send-mail-every-3-hours': {
        'task': 'django_weather_reminder.tasks.send_mail_every_n_hours',
        'schedule': crontab(hour='*/3', minute='5'),
        'args': (3,)
    },
    'send-mail-every-6-hours': {
        'task': 'django_weather_reminder.tasks.send_mail_every_n_hours',
        'schedule': crontab(hour='*/6', minute='5'),
        'args': (6,)
    },
    'send-mail-every-12-hours': {
        'task': 'django_weather_reminder.tasks.send_mail_every_n_hours',
        'schedule': crontab(hour='*/12', minute='5'),
        'args': (12,)
    },
    'send-mail-every-midnight': {
        'task': 'django_weather_reminder.tasks.send_mail_every_n_hours',
        'schedule': crontab(hour='0', minute='5'),
        'args': (24,)
    }
}
