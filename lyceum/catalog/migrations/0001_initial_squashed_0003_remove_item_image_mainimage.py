# Generated by Django 4.2.5 on 2023-10-31 23:33

import catalog.validators
import ckeditor_uploader.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    replaces = [
        ("catalog", "0001_initial"),
        ("catalog", "0002_item_is_on_main_alter_item_tags"),
        ("catalog", "0003_remove_item_image_mainimage"),
    ]

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Название элемента. Уникально для элементов одной модели",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Показывает, будет ли элемент опубликован",
                        verbose_name="опубликовано",
                    ),
                ),
                (
                    "weight",
                    models.IntegerField(
                        default=100,
                        help_text="Вес категории. Имеет значение от 0 до 32767",
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(32768),
                        ],
                        verbose_name="Вес",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Слаг элемента. Уникален для каждой категории. Содержит только символы латиницы, цифры и символы `-_`",
                        max_length=200,
                        unique=True,
                        verbose_name="слаг",
                    ),
                ),
                (
                    "normalized_name",
                    models.CharField(
                        help_text="ты не должен это видеть",
                        max_length=150,
                        unique=True,
                        verbose_name="нормализованное имя",
                    ),
                ),
            ],
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "категории",
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Название элемента. Уникально для элементов одной модели",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Показывает, будет ли элемент опубликован",
                        verbose_name="опубликовано",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default=None,
                        help_text="Главная картинка товара",
                        upload_to="catalog/images/",
                        verbose_name="главная картинка",
                    ),
                ),
                (
                    "text",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        help_text="Описание товара. Обязательно содержит слова `Роскошно` или `Превосходно`",
                        validators=[
                            catalog.validators.ValidateMustContain(
                                "превосходно", "роскошно"
                            )
                        ],
                        verbose_name="текст",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        help_text="Категория товара. Одна из списка созданных категорий",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="catalog.category",
                        verbose_name="категория",
                    ),
                ),
                (
                    "is_on_main",
                    models.BooleanField(
                        default=False,
                        help_text="Отображать элемент на главной странице?",
                        verbose_name="опубликовано на главной",
                    ),
                ),
            ],
            options={
                "verbose_name": "товар",
                "verbose_name_plural": "товары",
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Название элемента. Уникально для элементов одной модели",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Показывает, будет ли элемент опубликован",
                        verbose_name="опубликовано",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Слаг элемента. Уникален для каждого тега. Содержит только символы латиницы, цифры и символы `-_`",
                        max_length=200,
                        unique=True,
                        verbose_name="слаг",
                    ),
                ),
                (
                    "normalized_name",
                    models.CharField(
                        help_text="ты не должен это видеть",
                        max_length=150,
                        unique=True,
                        verbose_name="нормализованное имя",
                    ),
                ),
            ],
            options={
                "verbose_name": "тег",
                "verbose_name_plural": "теги",
            },
        ),
        migrations.CreateModel(
            name="ItemImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default=None,
                        help_text="Главная картинка товара",
                        upload_to="catalog/images/",
                        verbose_name="главная картинка",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.item",
                    ),
                ),
            ],
            options={
                "verbose_name": "картинка товара",
                "verbose_name_plural": "картинки товара",
            },
        ),
        migrations.AddField(
            model_name="item",
            name="tags",
            field=models.ManyToManyField(
                help_text="Теги товара. Их может быть сколько угодно, но хотя бы один",
                related_name="items",
                to="catalog.tag",
                verbose_name="теги",
            ),
        ),
        migrations.RemoveField(
            model_name="item",
            name="image",
        ),
        migrations.CreateModel(
            name="MainImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default=None,
                        help_text="Главная картинка товара",
                        upload_to="catalog/images/",
                        verbose_name="главная картинка",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.item",
                    ),
                ),
            ],
            options={
                "verbose_name": "главная картинка товара",
                "verbose_name_plural": "главные картинки товара",
            },
        ),
    ]