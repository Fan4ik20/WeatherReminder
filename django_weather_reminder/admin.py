from django.contrib import admin

from django_weather_reminder.models import (
    Country, City, User, Subscription, CurrentWeather
)

admin.site.register(Country)
admin.site.register(City)
admin.site.register(User)
admin.site.register(Subscription)
admin.site.register(CurrentWeather)
