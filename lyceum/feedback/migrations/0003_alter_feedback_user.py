# Generated by Django 4.2.5 on 2023-11-07 18:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "feedback",
            "0002_feedback_name_feedback_status_feedback_user_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
