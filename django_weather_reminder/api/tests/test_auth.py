from django.test import TestCase
from django.urls import reverse_lazy

from django_weather_reminder.tests import factories
from django_weather_reminder.models import User


class TestAuth(TestCase):
    @staticmethod
    def _create_test_user_for_login(username: str, password: str) -> User:
        test_user = factories.UserFactory(username=username)
        test_user.set_password(password)
        test_user.save()

        return test_user

    def test_login(self) -> None:
        test_username, test_password = 'test', 'test_password'

        self._create_test_user_for_login(
            test_username, test_password
        )

        response = self.client.post(
            reverse_lazy('token_obtain_pair'),
            {'username': test_username, 'password': test_password}
        )

        content = response.content

        self.assertIn(b'refresh', content)
        self.assertIn(b'access', content)

        self.assertEqual(200, response.status_code)

    def test_login_with_wrong_data(self) -> None:
        test_username, test_password = 'test', 'test_password'

        self._create_test_user_for_login(
            test_username, test_password
        )

        response = self.client.post(
            reverse_lazy('token_obtain_pair'),
            {'username': test_username, 'password': 'wrong_password'}
        )

        self.assertEqual(401, response.status_code)
        self.assertJSONEqual(
            response.content,
            {"detail": "No active account found with the given credentials"}
        )

    def test_registration_with_incomplete_fields(self) -> None:
        incomplete_data = {
            'username': 'suer',
            'password': 'test_password',
            'email': 'test@test.com'
        }

        response = self.client.post(
            reverse_lazy('registration'), incomplete_data
        )

        self.assertEqual(400, response.status_code)
        self.assertJSONEqual(
            response.content,
            {"password2": ["This field is required."]}
        )

    def test_registration_with_wrong_data(self) -> None:
        wrong_data = {
            'username': 'suer',
            'password': 'test_password',
            'password2': 'wrong_password',
            'email': 'test@test.com'
        }

        response = self.client.post(
            reverse_lazy('registration'), wrong_data
        )

        self.assertEqual(400, response.status_code)
        self.assertJSONEqual(response.content, ["The passwords should match!"])

    def test_registration(self) -> None:
        registration_data = {
            'username': 'suer',
            'password': 'suer_password',
            'password2': 'suer_password',
            'email': 'suer@gmail.com'
        }

        response = self.client.post(
            reverse_lazy('registration'), registration_data
        )

        self.assertEqual(201, response.status_code)

        self.assertIn(b'refresh', response.content)
        self.assertIn(b'access', response.content)

        self.assertTrue(User.users.check_exists(registration_data['username']))
