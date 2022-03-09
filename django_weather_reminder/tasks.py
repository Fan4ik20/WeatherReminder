from DjangoWeatherReminder.celery import app

from django_weather_reminder import service


@app.task(priority=0)
def fill_active_cities() -> None:
    service.fill_weather_active_cities()


@app.task(priority=9)
def send_mail_every_n_hours(n: int) -> None:
    service.send_users_weather_forecast(n)
