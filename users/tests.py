from django.contrib.auth.hashers import make_password
from django.test import TestCase
from users.models import User, UserType


class UserViewsTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@test.com",
            password=make_password("test_password"),
            user_type=UserType.USER,
        )

    def test_login_succeeds(self):
        response = self.client.post(
            path="/api/users/login",
            data={"email": "john@example.com", "password": "test_password"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["user_type"], "User")
        self.assertTrue("access" in data)
        self.assertTrue("refresh" in data)

    def test_login_fails_on_incorrect_password(self):
        response = self.client.post(
            path="/api/users/login",
            data={"email": "john@example.com", "password": "wrong_password"},
        )
        self.assertEqual(response.status_code, 401)

    def test_login_fails_on_email_that_does_not_exist(self):
        response = self.client.post(
            path="/api/users/login",
            data={"email": "does_not_exist@example.com", "password": "test_password"},
        )
        self.assertEqual(response.status_code, 401)

    def test_create_user_succeeds(self):
        payload = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com",
            "password": "jane_password",
        }
        response = self.client.post(path="/api/users/signup", data=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_user_fails_on_non_unique_email(self):
        payload = {
            "first_name": "Another John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "another_password",
        }
        response = self.client.post(path="/api/users/signup", data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["email"], ["Email already exists."])
