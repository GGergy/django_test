from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Item, ItemImage, Tag


class TestDBAnswer(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cat = Category.objects.create(
            name="123",
            slug="123zxc",
        )
        cls.tag = Tag.objects.create(
            name="123",
            slug="123zxc",
        )
        cls.item = Item.objects.create(
            name="123",
            category=cls.cat,
            is_on_main=True,
            text="роскошно btw",
        )
        cls.img = ItemImage.objects.create(
            image="same.png",
            item=cls.item,
        )
        cls.item.tags.add(cls.tag)

    def test_optimized(self):
        response = self.client.get(reverse("homepage:main"))
        item = response.context["items"][0]

        exist = (
            "name",
            "text",
            "category_id",
        )
        prefetch = ("tags",)
        not_exist = (
            "is_on_main",
            "created_at",
            "updated_at",
            "is_published",
            "is_on_main",
        )

        check_dict = item.__dict__

        for field in exist:
            self.assertIn(field, check_dict)

        for field in prefetch:
            self.assertIn(field, check_dict["_prefetched_objects_cache"])

        for field in not_exist:
            self.assertNotIn(field, check_dict)


__all__ = []
