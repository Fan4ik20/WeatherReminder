import requests

import os


class OpenWeatherMapParser:
    def __init__(self, api_key: str = os.getenv('OPENWEATHERMAP_KEY')):
        self._api_key = api_key
        self._base_onecall_url = (
            'https://api.openweathermap.org/data/2.5/onecall'
        )
        self._base_current_url = (
            'https://api.openweathermap.org/data/2.5/weather'
        )

    def _send_city_request(self, city_lat: float, city_lon: float) -> dict:
        params = {
            'units': 'metric', 'appid': self._api_key,
            'exclude': 'current,minutely', 'lat': city_lat, 'lon': city_lon,
        }
        forecast_data = requests.get(
            self._base_onecall_url, params=params
        ).json()

        return forecast_data

    @staticmethod
    def _add_forecast_to_list(
            weather_forecasts_data: list[dict], resulted_list: list
    ) -> None:
        for forecast_data in weather_forecasts_data:
            resulted_list.append(
                {
                    'weather_status': forecast_data['weather'][0]['main'],
                    'weather_description':
                        forecast_data['weather'][0]['description'],
                    'temp': forecast_data['temp'],
                    'feels_like': forecast_data['feels_like'],
                    'date_time': forecast_data['dt'],
                    'pressure': forecast_data['pressure'],
                    'humidity': forecast_data['humidity'],
                    'wind_speed': forecast_data['wind_speed']
                }
            )

    def parse_city_weather_forecast(
            self, city_lat: float, city_lon: float
    ) -> dict:
        forecasts_data = self._send_city_request(city_lat, city_lon)

        hourly_forecasts: list[dict] = []
        daily_forecasts: list[dict] = []

        self._add_forecast_to_list(forecasts_data['hourly'], hourly_forecasts)
        self._add_forecast_to_list(forecasts_data['daily'], daily_forecasts)

        convenient_weather_forecasts = {
            'hourly_forecasts': hourly_forecasts,
            'daily_forecasts': daily_forecasts
        }

        return convenient_weather_forecasts

    def _send_current_weather_request(
            self, city_lat: float, city_lon: float
    ) -> dict:
        params = {
            'units': 'metric', 'appid': self._api_key,
            'lat': city_lat, 'lon': city_lon
        }

        current_forecast_data = requests.get(
            self._base_current_url, params=params
        ).json()

        return current_forecast_data

    @staticmethod
    def _build_current_forecast_dict(current_forecast_data: dict) -> dict:
        convenient_forecast = {
            'weather_status': current_forecast_data['weather'][0]['main'],
            'weather_description':
                current_forecast_data['weather'][0]['description'],
            'temp': current_forecast_data['main']['temp'],
            'feels_like': current_forecast_data['main']['feels_like'],
            'date_time': current_forecast_data['dt'],
            'pressure': current_forecast_data['main']['pressure'],
            'humidity': current_forecast_data['main']['humidity'],
            'wind_speed': current_forecast_data['wind']['speed']
        }

        return convenient_forecast

    def parse_city_current_weather(
            self, city_lat: float, city_lon: float
    ) -> dict:
        current_forecast_data = self._send_current_weather_request(
            city_lat, city_lon
        )

        convenient_current_forecast = self._build_current_forecast_dict(
            current_forecast_data
        )

        return convenient_current_forecast
