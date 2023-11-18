from django.core.exceptions import ValidationError
from django.test import TestCase

from catalog.models import Category, Item, Tag


class MyStaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = Category.objects.create(
            name="Test Category",
            slug="test-category-slug",
        )
        cls.tag = Tag.objects.create(name="Test Tag", slug="test-tag-slug")

    def test_create_valid_item(self):
        item_count = Item.objects.count()
        self.item = Item(
            name="Test Item",
            category=self.category,
            text="Роскошно",
        )
        self.item.full_clean()
        self.item.save()
        self.assertEqual(item_count + 1, Item.objects.count())

    def test_create_invalid_item(self):
        item_count = Item.objects.count()
        with self.assertRaises(ValidationError):
            self.item = Item(
                name="Test Item",
                category=self.category,
                text="плохо ужасно",
            )
            self.item.full_clean()
            self.item.save()
        self.assertEqual(item_count, Item.objects.count())

    def test_create_invalid_tag_slug_unique(self):
        tags_count = Tag.objects.count()
        with self.assertRaises(ValidationError):
            self.tag = Tag(name="Test Tag 2", slug="test-tag-slug")
            self.tag.full_clean()
            self.tag.save()
        self.assertEqual(tags_count, Tag.objects.count())

    def test_create_invalid_tag_slug_content(self):
        tags_count = Tag.objects.count()
        with self.assertRaises(ValidationError):
            self.tag = Tag(
                name="Test Tag 2",
                slug="слаг на русском да еще и со спецсимволами ужас ваще((((",
            )
            self.tag.full_clean()
            self.tag.save()
        self.assertEqual(tags_count, Tag.objects.count())

    def test_create_invalid_category_slug_content(self):
        cat_count = Category.objects.count()
        with self.assertRaises(ValidationError):
            self.cat = Category(
                name="Test Tag 2",
                slug="слаг на русском да еще и со спецсимволами ужас ваще((((",
            )
            self.cat.full_clean()
            self.cat.save()
        self.assertEqual(cat_count, Category.objects.count())

    def test_create_invalid_category_slug_unique(self):
        cat_count = Category.objects.count()
        with self.assertRaises(ValidationError):
            self.cat = Category(
                name="Test Category 2",
                slug="test-category-slug",
            )
            self.cat.full_clean()
            self.cat.save()
        self.assertEqual(cat_count, Category.objects.count())

    def test_create_invalid_category_weight(self):
        cat_count = Category.objects.count()
        with self.assertRaises(ValidationError):
            self.cat = Category(
                name="Test Category 2",
                slug="test-category-slug2",
                weight=0,
            )
            self.cat.full_clean()
            self.cat.save()
        self.assertEqual(cat_count, Category.objects.count())

    def test_create_same_tag(self):
        Tag.objects.create(name="Тестовый тег", slug="test-tag-slug123456")
        tags_count = Tag.objects.count()
        with self.assertRaises(ValidationError):
            self.tag = Tag(
                name="TecтoВЫй     !!!!!!тeГГГ.........",
                slug="zxczxczxczxc123123123",
            )
            self.tag.full_clean()
            self.tag.save()
        self.assertEqual(tags_count, Tag.objects.count())

    def test_create_same_category(self):
        Category.objects.create(
            name="Тестовая категория",
            slug="test-tag-slug123456789",
        )
        cat_count = Category.objects.count()
        with self.assertRaises(ValidationError):
            self.cat = Category(
                name="тEEEEсcтовaякатEEEEгггОоОoриЯ...!!!!",
                slug="zxczxczxczxc123123123123123",
            )
            self.cat.full_clean()
            self.cat.save()
        self.assertEqual(cat_count, Category.objects.count())


__all__ = []
