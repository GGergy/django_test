from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    def test_homepage(self):
        response = self.client.get(reverse("homepage:main"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_coffee_status_code(self):
        response = self.client.get(reverse("homepage:coffee"))
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)


__all__ = []
