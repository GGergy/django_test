# Generated by Django 4.2.5 on 2023-11-08 16:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    replaces = [
        ("feedback", "0005_alter_statuslog_status_from_and_more"),
        (
            "feedback",
            "0006_alter_feedback_options_alter_feedback_created_on_and_more",
        ),
        ("feedback", "0007_rename_status_from_statuslog_from_and_more"),
        ("feedback", "0008_rename_timestamp_statuslog_timestamp_and_more"),
        (
            "feedback",
            "0009_remove_statuslog_from_remove_statuslog_to_and_more",
        ),
        ("feedback", "0010_remove_feedback_user"),
        ("feedback", "0011_rename_from_status_statuslog_from_and_more"),
        ("feedback", "0012_rename_from_statuslog_from"),
        ("feedback", "0013_alter_feedback_name"),
        ("feedback", "0014_rename_from_statuslog_from"),
    ]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("feedback", "0004_alter_feedback_user"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="feedback",
            options={
                "verbose_name": "фидбэк",
                "verbose_name_plural": "фидбэки",
            },
        ),
        migrations.AlterField(
            model_name="feedback",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="дата создания"
            ),
        ),
        migrations.AlterField(
            model_name="feedback",
            name="mail",
            field=models.EmailField(max_length=254, verbose_name="почта"),
        ),
        migrations.AlterField(
            model_name="feedback",
            name="name",
            field=models.CharField(
                max_length=150, verbose_name="имя пользователя"
            ),
        ),
        migrations.AlterField(
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
                verbose_name="статус вопроса",
            ),
        ),
        migrations.AlterField(
            model_name="feedback",
            name="text",
            field=models.TextField(verbose_name="текст сообщения"),
        ),
        migrations.RenameField(
            model_name="statuslog",
            old_name="status_from",
            new_name="From",
        ),
        migrations.RenameField(
            model_name="statuslog",
            old_name="time",
            new_name="timestamp",
        ),
        migrations.AlterField(
            model_name="statuslog",
            name="timestamp",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.RenameField(
            model_name="statuslog",
            old_name="status_to",
            new_name="to",
        ),
        migrations.RenameField(
            model_name="statuslog",
            old_name="user",
            new_name="user",
        ),
        migrations.AlterField(
            model_name="statuslog",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RemoveField(
            model_name="statuslog",
            name="From",
        ),
        migrations.RemoveField(
            model_name="statuslog",
            name="to",
        ),
        migrations.AlterField(
            model_name="feedback",
            name="status",
            field=models.CharField(
                choices=[
                    ("получено", "получено"),
                    ("в обработке", "в обработке"),
                    ("ответ дан", "ответ дан"),
                ],
                default="получено",
                max_length=15,
                verbose_name="статус вопроса",
            ),
        ),
        migrations.RemoveField(
            model_name="feedback",
            name="user",
        ),
        migrations.AddField(
            model_name="statuslog",
            name="to",
            field=models.CharField(
                choices=[
                    ("получено", "получено"),
                    ("в обработке", "в обработке"),
                    ("ответ дан", "ответ дан"),
                ],
                default="получено",
                max_length=15,
            ),
        ),
        migrations.AlterField(
            model_name="feedback",
            name="name",
            field=models.CharField(
                blank=True,
                max_length=150,
                null=True,
                verbose_name="имя пользователя",
            ),
        ),
        migrations.AddField(
            model_name="statuslog",
            name="from",
            field=models.CharField(
                choices=[
                    ("получено", "получено"),
                    ("в обработке", "в обработке"),
                    ("ответ дан", "ответ дан"),
                ],
                default="получено",
                max_length=15,
            ),
        ),
    ]
