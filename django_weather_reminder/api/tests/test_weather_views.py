from rest_framework.test import APITestCase
from django.urls import reverse_lazy

from django_weather_reminder.tests import factories
from django_weather_reminder.models import City, Country, Subscription


class TestCountryViewSet(APITestCase):
    def setUp(self) -> None:
        self.test_country = factories.CountryFactory()
        self.country_list_url = reverse_lazy('country-list')

    @staticmethod
    def _build_expected_json_detail(expected_country: Country) -> dict:
        expected_json = {
            'id': expected_country.pk,
            'name': expected_country.name,
            'code': expected_country.code
        }

        return expected_json

    def _build_expected_json_list(
            self, expected_countries: list[Country]
    ) -> list[dict]:
        expected_json = [
            self._build_expected_json_detail(country)
            for country in expected_countries
        ]

        return expected_json

    def test_get_countries(self) -> None:
        expected_json = self._build_expected_json_list([self.test_country])

        response = self.client.get(self.country_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_json)

    def test_search_countries(self) -> None:
        matched_countries = [
            factories.CountryFactory(name='_searched'),
            factories.CountryFactory(name='_search')
        ]

        expected_json = self._build_expected_json_list(matched_countries)

        response = self.client.get(
            f'{self.country_list_url}?search=_sear'
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_json)

    def test_get_detail_country(self) -> None:
        expected_json = self._build_expected_json_detail(
            self.test_country
        )

        response = self.client.get(
            reverse_lazy('country-detail', args=(self.test_country.pk,))
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_json)

    def test_get_non_existent_country_detail(self) -> None:
        expected_json = {'detail': 'Not found.'}

        response = self.client.get(
            reverse_lazy('country-detail', args=(1648,))
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, expected_json)


class TestCityViewSet(APITestCase):
    @staticmethod
    def _create_test_cities(country: Country) -> list[City]:
        test_cities = [
            factories.CityFactory(active=True, country=country),
            factories.CityFactory(active=True, country=country),
            factories.CityFactory(country=country)
        ]

        return test_cities

    def setUp(self) -> None:
        self.test_country = factories.CountryFactory()
        self.test_cities = self._create_test_cities(self.test_country)
        self.test_city = self.test_cities[0]

        self.city_list_url = reverse_lazy(
            'city-list', args=(self.test_country.pk,)
        )

    @staticmethod
    def _build_expected_json_detail(expected_city: City) -> dict:
        expected_json = {
            'id': expected_city.pk,
            'name': expected_city.name,
            'lat': float(expected_city.lat),
            'lon': float(expected_city.lon),
            'active': expected_city.active,
            'country': expected_city.country.name
        }

        return expected_json

    def _build_expected_json_list(
            self, expected_cities: list[City]
    ) -> list[dict]:
        expected_json = [
            self._build_expected_json_detail(city) for city in expected_cities
        ]

        return expected_json

    def test_get_cities_list(self) -> None:
        expected_json = self._build_expected_json_list(self.test_cities)

        response = self.client.get(
            self.city_list_url
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_json)

    def test_get_active_cities(self) -> None:
        active_cities = self.test_cities[:2]

        expected_json = self._build_expected_json_list(active_cities)

        response = self.client.get(
            f'{self.city_list_url}?active=true'
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_json)

    def test_city_search(self) -> None:
        matched_cities = [
            factories.CityFactory(name='_testName', country=self.test_country),
            factories.CityFactory(name='_testTest', country=self.test_country)
        ]

        expected_json = self._build_expected_json_list(matched_cities)

        response = self.client.get(
            f'{self.city_list_url}?search=_test'
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_json)

    def test_get_detail_city(self) -> None:
        expected_json = self._build_expected_json_detail(self.test_city)

        response = self.client.get(
            reverse_lazy(
                'city-detail', args=(self.test_country.pk, self.test_city.pk)
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_json)

    def test_get_non_existent_city_detail(self) -> None:
        expected_json = {'detail': 'Not found.'}

        response = self.client.get(
            reverse_lazy(
                'city-detail', args=(self.test_country.pk, 404)
            )
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, expected_json)

    def test_get_city_detail_with_wrong_country(self) -> None:
        expected_json = {'detail': 'Not found.'}

        response = self.client.get(
            reverse_lazy('city-detail', args=(404, self.test_city.pk))
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, expected_json)


class TestSubscriptionViewSet(APITestCase):
    def _create_user(self) -> None:
        self.test_user = factories.UserFactory()
        self.test_user.set_password('testTest')
        self.test_user.save()

    def _create_subscriptions(self) -> None:
        self.test_country = factories.CountryFactory()

        first_city = factories.CityFactory(country=self.test_country)
        second_city = factories.CityFactory(country=self.test_country)

        Subscription.subscriptions.create(
            user=self.test_user, city=first_city, frequency=3
        )

        Subscription.subscriptions.create(
            user=self.test_user, city=second_city, frequency=6
        )

    def _login_user(self) -> None:
        data_to_login = {
            'username': self.test_user.username,
            'password': 'testTest'
        }

        response = self.client.post(
            reverse_lazy('token_obtain_pair'), data_to_login
        )

        self.token = response.json()['access']

    def _create_user_and_save_credentials(self) -> None:
        self._create_user()
        self._create_subscriptions()
        self._login_user()

    def setUp(self) -> None:
        self._create_user_and_save_credentials()

        self.subscription_list_url = reverse_lazy(
            'subscription-list'
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    @staticmethod
    def _build_expected_json_detail(subscription: Subscription) -> dict:
        expected_json = {
            'id': subscription.pk,
            'user': subscription.user.username,
            'frequency': subscription.frequency,
            'city': subscription.city.pk
        }

        return expected_json

    def _build_expected_json_list(
            self, expected_subscriptions: list[Subscription]
    ) -> list[dict]:

        expected_json = [
            self._build_expected_json_detail(subscription)
            for subscription in expected_subscriptions
        ]

        return expected_json

    def test_get_unauthorized_user_subscription_list(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=None)

        expected_json = {
            'detail': 'Authentication credentials were not provided.'
        }

        response = self.client.get(
            self.subscription_list_url
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, expected_json)

    def test_get_user_subscription_list(self) -> None:
        expected_json = self._build_expected_json_list(
            self.test_user.subscriptions.all()
        )

        response = self.client.get(self.subscription_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_json)

    def test_get_user_subscription_detail(self) -> None:
        tested_subscription = self.test_user.subscriptions.first()

        expected_json = self._build_expected_json_detail(
            tested_subscription
        )

        response = self.client.get(
            reverse_lazy('subscription-detail', args=(tested_subscription.pk,))
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_json)

    def test_get_user_non_existent_subscription_detail(self) -> None:
        expected_json = {'detail': 'Not found.'}

        response = self.client.get(
            reverse_lazy('subscription-detail', args=(404,))
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, expected_json)

    def test_post_user_subscription(self) -> None:
        new_city = factories.CityFactory(country=self.test_country)

        subscription_data = {
            'city': new_city.pk,
            'frequency': 6
        }

        response = self.client.post(
            self.subscription_list_url, subscription_data
        )

        received_json_values = response.json().values()

        self.assertEqual(response.status_code, 201)

        self.assertIn(new_city.pk, received_json_values)
        self.assertIn(self.test_user.username, received_json_values)
        self.assertIn(6, received_json_values)

    def test_post_with_wrong_field(self):
        expected_json = ["You passed wrong fields!"]

        new_city = factories.CityFactory(country=self.test_country)

        wrong_subscription_data = {
            'country': new_city.pk,
            'frequency': 6
        }

        response = self.client.post(
            self.subscription_list_url, wrong_subscription_data
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, expected_json)

    def test_post_already_existent_city_subscription(self):
        expected_json = ['You can only subscribe to one city once!']

        existent_subscription = self.test_user.subscriptions.first()

        wrong_data = {
            'city': existent_subscription.city.pk,
            'frequency': 3
        }

        response = self.client.post(
            self.subscription_list_url, wrong_data
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, expected_json)

    def test_post_user_subscription_with_wrong_frequency(self) -> None:
        expected_json = {
            'frequency':
                ['Value must be in the given values set - {1, 3, 6, 24, 12}']
        }

        new_city = factories.CityFactory(country=self.test_country)

        wrong_data = {
            'city': new_city.pk,
            'frequency': 4,
        }

        response = self.client.post(
            self.subscription_list_url, wrong_data
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, expected_json)

    def test_patch_user_subscription(self) -> None:
        old_subscription = self.test_user.subscriptions.first()

        patch_data = {
            'frequency': 24
        }

        response = self.client.patch(
            reverse_lazy('subscription-detail', args=(old_subscription.pk,)),
            patch_data
        )

        received_json_values = response.json().values()

        self.assertEqual(response.status_code, 200)

        self.assertIn(old_subscription.city.pk, received_json_values)
        self.assertIn(old_subscription.user.username, received_json_values)
        self.assertIn(24, received_json_values)
