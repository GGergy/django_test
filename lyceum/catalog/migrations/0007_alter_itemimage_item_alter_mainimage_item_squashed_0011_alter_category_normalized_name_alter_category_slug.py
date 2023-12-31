# Generated by Django 4.2.5 on 2023-10-31 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    replaces = [
        ("catalog", "0007_alter_itemimage_item_alter_mainimage_item"),
        ("catalog", "0008_alter_category_normalized_name"),
        ("catalog", "0009_alter_category_normalized_name_and_more"),
        ("catalog", "0010_alter_category_slug_alter_tag_normalized_name"),
        ("catalog", "0011_alter_category_normalized_name_alter_category_slug"),
    ]

    dependencies = [
        ("catalog", "0006_alter_mainimage_item"),
    ]

    operations = [
        migrations.AlterField(
            model_name="itemimage",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="catalog.item",
            ),
        ),
        migrations.AlterField(
            model_name="mainimage",
            name="item",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="main_image",
                to="catalog.item",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="normalized_name",
            field=models.CharField(
                default=None,
                help_text="ты не должен это видеть",
                max_length=150,
                verbose_name="нормализованное имя",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="normalized_name",
            field=models.CharField(
                blank=True,
                default=None,
                help_text="ты не должен это видеть",
                max_length=150,
                verbose_name="нормализованное имя",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="normalized_name",
            field=models.CharField(
                blank=True,
                default=None,
                help_text="ты не должен это видеть",
                max_length=150,
                verbose_name="нормализованное имя",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(
                help_text="Слаг элемента. Уникален для каждой категории. Содержит только символы латиницы, цифры и символы `-_`",
                max_length=200,
                null=True,
                verbose_name="слаг",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="normalized_name",
            field=models.CharField(
                default=None,
                help_text="ты не должен это видеть",
                max_length=150,
                null=True,
                verbose_name="нормализованное имя",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="normalized_name",
            field=models.CharField(
                default=None,
                help_text="ты не должен это видеть",
                max_length=150,
                null=True,
                verbose_name="нормализованное имя",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(
                help_text="Слаг элемента. Уникален для каждой категории. Содержит только символы латиницы, цифры и символы `-_`",
                max_length=200,
                unique=True,
                verbose_name="слаг",
            ),
        ),
    ]
