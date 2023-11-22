from datetime import datetime, timedelta
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.signing import TimestampSigner
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from users.models import Profile


class TestRegistration(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            password="zxczxc123",
            email="zxc@ya.ru",
            username="testname",
            is_active=False,
        )

    def test_registration(self):
        users = User.objects.count()
        self.client.post(
            reverse("users:signup"),
            data={
                "username": "name",
                "password1": "zxc123123",
                "password2": "zxc123123",
                "email": "zxczxc@ya.ru",
            },
        )
        self.assertEqual(users + 1, User.objects.count())

    @patch("django.utils.timezone.now")
    def test_activate(self, mock_timezone):
        dt = datetime.now() + timedelta(days=1)
        dt = dt.replace(tzinfo=timezone.utc)
        mock_timezone.return_value = dt
        self.client.post(
            reverse(
                "users:activate",
                args=(TimestampSigner().sign("testname"),),
            ),
        )
        self.assertEqual(
            User.objects.get(username="testname").is_active,
            False,
        )

    def test_normal_activate(self):
        self.client.post(
            reverse(
                "users:activate",
                args=(TimestampSigner().sign("testname"),),
            ),
        )
        self.assertEqual(User.objects.get(username="testname").is_active, True)


class TestBirthdayUsers(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_birthday = User.objects.create_user(
            username="testname_b",
            first_name="name_b",
            email="testmail1@ya.ru",
            password="testPASS123",
            is_active=False,
        )
        cls.profile_birthday = Profile.objects.create(
            user=cls.user_birthday,
            birthday=datetime.now().date(),
        )

        cls.user_not_birthday = User.objects.create_user(
            username="testname_nb",
            first_name="name_nb",
            email="testmail2@ya.ru",
            password="testPASS123",
            is_active=False,
        )
        cls.profile_not_birthday = Profile.objects.create(
            user=cls.user_not_birthday,
            birthday="2023-11-21",
        )

    def test_context(self):
        response = self.client.get(reverse("homepage:main"))
        self.assertIn("birthday_users", response.context)

    def test_len_context(self):
        response = self.client.get(reverse("homepage:main"))
        birthday_users = response.context["birthday_users"]

        self.assertEqual(len(birthday_users), 1)

    def test_correct_birthday(self):
        response = self.client.get(reverse("homepage:main"))
        birthday_users = response.context["birthday_users"]

        self.assertEqual(birthday_users[0].user.first_name, "name_b")
        self.assertEqual(birthday_users[0].user.email, "testmail1@ya.ru")

    def test_uncorrect_birthday(self):
        response = self.client.get(reverse("homepage:main"))
        birthday_users = response.context["birthday_users"]

        for i in birthday_users:
            self.assertNotEqual(i.user.first_name, "name_nb")
            self.assertNotEqual(i.user.email, "testmail2@ya.ru")


__all__ = []
