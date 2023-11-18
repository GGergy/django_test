from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized

from catalog.models import Category, Item, Tag


class TestResponseContext(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pub_cat = Category.objects.create(
            name="123",
            is_published=True,
            slug="123zxc",
        )
        cls.unpub_cat = Category.objects.create(
            name="456",
            is_published=False,
            slug="456zxc",
        )
        cls.pub_tag = Tag.objects.create(
            name="123",
            is_published=True,
            slug="123zxc",
        )
        cls.unpub_tag = Tag.objects.create(
            name="456",
            is_published=False,
            slug="456zxc",
        )

    @parameterized.expand(
        (
            (True, True, 1),
            (True, False, 0),
            (False, True, 0),
            (False, False, 0),
            (True, True, 1),
        ),
    )
    def test_catalog_items(
        self,
        is_published,
        category_pub,
        item_count,
    ):
        self.item = Item(
            name="123",
            is_published=is_published,
            category=self.get_category(category_pub),
            text="роскошно btw",
        )
        self.item.full_clean()
        self.item.save()

        response = self.client.get(reverse("catalog:main"))
        items = response.context["items"]
        self.assertEqual(len(items), item_count)

    @parameterized.expand(
        (
            (True, True, True, 1),
            (True, False, True, 0),
            (False, True, True, 0),
            (False, False, True, 0),
            (False, False, False, 0),
            (True, True, False, 0),
            (False, True, False, 0),
            (True, False, False, 0),
        ),
    )
    def test_on_main(self, is_on_main, is_published, category_pub, item_count):
        self.item = Item(
            name="123",
            is_published=is_published,
            category=self.get_category(category_pub),
            is_on_main=is_on_main,
            text="роскошно btw",
        )
        self.item.full_clean()
        self.item.save()
        response = self.client.get(reverse("homepage:main"))
        items = response.context["items"]
        self.assertEqual(len(items), item_count)

    def test_for_danya(self):
        pass

    def test_context_types(self):
        self.item = Item(
            name="123",
            is_published=True,
            category=self.get_category(True),
            is_on_main=True,
            text="роскошно btw",
        )
        self.item.full_clean()
        self.item.save()
        response = self.client.get(reverse("homepage:main"))
        items = response.context["items"]
        self.assertIsInstance(items[0], Item)
        response = self.client.get(reverse("catalog:main"))
        items = response.context["items"]
        self.assertIsInstance(items[0], Item)

    def get_category(self, is_published):
        if is_published:
            return self.pub_cat
        return self.unpub_cat

    def get_tag(self, is_published):
        if is_published:
            return self.pub_tag
        return self.unpub_tag


__all__ = []
