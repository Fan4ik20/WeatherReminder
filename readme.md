# Overview
This is a small web application based on the DRF,  
which is provided the API, through which you can subscribe  
to receive the current weather forecast.

## Requirements
- Python 3.10
- Redis server
- All modules requirements are specified in the requirements.txt file.  
You can install it via command `pip install -r requirements.txt`

## Installation. Launching
#### Installation
- Install all requirements
- Specify a list of env variables in the .env file:
  - SECRET_KEY
  - OPENWEATHERMAP_KEY
  - DB_NAME
  - DB_HOST
  - DB_PORT
  - DB_USER
  - DB_PASSWORD
  - EMAIL_HOST_USER
  - EMAIL_HOST_PASSWORD
  - REDIS_HOST
  - REDIS_PORT
- Create migrations for django_weather_reminder app via command  
`python manage.py makemigrations django_weather_reminder`
- Migrate database via command  
`python manage.py migrate`
#### Launching
- To start the server, use the command  
`python manage.py runserver`
- To start celery, use the command  
`celery -A DjangoWeatherReminder worker -l INFO`  
If you use Windows:  
`celery -A DjangoWeatherReminder worker -l INFO -P eventlet`
- To start beat, use the command  
`celery -A DjangoWeatherReminder beat -l INFO`
- Optional you can run flower to monitor the workers  
`celery -A DjangoWeatherReminder flower --port={PORT}`

## Management commands
You can use this command:
- `python manage.py fill_ukraine` - fills the database with cities in Ukraine
- `python manage.py delete_cities` - deletes all cities
- `python manage.py fill_weather_all_cities` - Fills in the current weather forecast for all cities

## Endpoints
All received data is presented in JSON format.
- `/swagger/` - API docs

- `/api/v1/`
  - `/countries/` - list of all countries
  - `/countries/<country_id>/` - information about particular country
  - `/countries/<country_id>/cities/` - list of all cities
  - `/countries/<country_id>/cities/<city_id>/` - information about particular city
  - `/accounts/subscriptions/` - list of user subscriptions to cities
  - `/accounts/subscriptions/<subscription_id>/` - information about particular subscription.
  - `/register/` - endpoint for registration
  - `/token/` - endpoint for token obtaining

## Links
https://my-django-weather-forecast-app.herokuapp.com/

## License
MDI
