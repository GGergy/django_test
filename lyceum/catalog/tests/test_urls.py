from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from parameterized import parameterized

from catalog.models import Category, Item, Tag


class TestUrls(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = Category.objects.create(
            name="Test Category",
            slug="test-category-slug",
        )
        cls.tag = Tag.objects.create(name="Test Tag", slug="test-tag-slug")
        Item.objects.create(
            name="test",
            category=cls.category,
            text="роскошно",
        )

    @parameterized.expand(
        [
            (
                "catalog:main",
                (),
            ),
            ("catalog:item_detail_site", (1,)),
            ("catalog:friday",),
            ("catalog:new",),
            ("catalog:unverified",),
        ],
    )
    def test_valid_urls(self, endpoint, args=None, kwargs=None):
        response = self.client.get(reverse(endpoint, args=args, kwargs=kwargs))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @parameterized.expand(
        [
            ("catalog:item_detail_site", ("zxc",)),
            ("catalog:item_detail_site", (-1,)),
        ],
    )
    def test_invalid_urls(self, endpoint, args):
        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse(endpoint, args=args))
            self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_invalid_pk(self):
        response = self.client.get(
            reverse("catalog:item_detail_site", args=(100000,)),
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


__all__ = []
