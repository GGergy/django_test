from datetime import datetime, timedelta
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.signing import TimestampSigner
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone


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
        self.client.post(reverse("users:activate", args=(TimestampSigner().sign("testname"),)))
        self.assertEqual(
            User.objects.get(username="testname").is_active,
            False,
        )

    def test_normal_activate(self):
        self.client.post(reverse("users:activate", args=(TimestampSigner().sign("testname"),)))
        self.assertEqual(User.objects.get(username="testname").is_active, True)

    
__all__ = []
