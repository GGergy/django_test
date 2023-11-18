from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    def test_page_about(self):
        response = self.client.get(reverse("about:main"))
        self.assertEqual(response.status_code, HTTPStatus.OK)


__all__ = []
