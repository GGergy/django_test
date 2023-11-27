# Generated by Django 4.2.5 on 2023-11-27 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0017_alter_itemimage_image_alter_mainimage_image"),
        ("users", "0005_delete_userproxy_user"),
        ("rating", "0005_alter_itemrating_item_alter_itemrating_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="itemrating",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ratings",
                to="catalog.item",
            ),
        ),
        migrations.AlterField(
            model_name="itemrating",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ratings",
                to="users.user",
            ),
        ),
    ]