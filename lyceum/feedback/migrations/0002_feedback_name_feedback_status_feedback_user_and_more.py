# Generated by Django 4.2.5 on 2023-11-07 17:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("feedback", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="feedback",
            name="name",
            field=models.CharField(default="as", max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="feedback",
            name="status",
            field=models.CharField(
                choices=[
                    ("rc", "получено"),
                    ("pr", "в обработке"),
                    ("an", "ответ дан"),
                ],
                default="rc",
                max_length=2,
            ),
        ),
        migrations.AddField(
            model_name="feedback",
            name="user",
            field=models.ForeignKey(
                default=345,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="feedback",
            name="created_on",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name="StatusLog",
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
                ("time", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "status_from",
                    models.CharField(
                        choices=[
                            ("rc", "получено"),
                            ("pr", "в обработке"),
                            ("an", "ответ дан"),
                        ],
                        max_length=2,
                        null=True,
                    ),
                ),
                (
                    "status_to",
                    models.CharField(
                        choices=[
                            ("rc", "получено"),
                            ("pr", "в обработке"),
                            ("an", "ответ дан"),
                        ],
                        max_length=2,
                        null=True,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
