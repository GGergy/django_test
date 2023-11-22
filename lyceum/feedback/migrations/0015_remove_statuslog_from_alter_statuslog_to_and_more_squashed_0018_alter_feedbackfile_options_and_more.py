# Generated by Django 4.2.5 on 2023-11-08 21:47

from django.db import migrations, models
import django.db.models.deletion
import feedback.models


class Migration(migrations.Migration):
    replaces = [
        ("feedback", "0015_remove_statuslog_from_alter_statuslog_to_and_more"),
        ("feedback", "0016_feedbackfile"),
        (
            "feedback",
            "0017_remove_feedback_mail_remove_feedback_name_and_more",
        ),
        ("feedback", "0018_alter_feedbackfile_options_and_more"),
    ]

    dependencies = [
        (
            "feedback",
            "0005_alter_statuslog_status_from_and_more_squashed_0014_rename_from_statuslog_from",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="statuslog",
            name="from",
        ),
        migrations.AlterField(
            model_name="statuslog",
            name="to",
            field=models.CharField(
                choices=[
                    ("получено", "получено"),
                    ("в обработке", "в обработке"),
                    ("ответ дан", "ответ дан"),
                ],
                max_length=15,
            ),
        ),
        migrations.AddField(
            model_name="statuslog",
            name="From",
            field=models.CharField(
                choices=[
                    ("получено", "получено"),
                    ("в обработке", "в обработке"),
                    ("ответ дан", "ответ дан"),
                ],
                db_column="from",
                default="получено",
                max_length=15,
            ),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name="feedback",
            name="mail",
        ),
        migrations.RemoveField(
            model_name="feedback",
            name="name",
        ),
        migrations.CreateModel(
            name="PersonalInfo",
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
                    "mail",
                    models.EmailField(max_length=254, verbose_name="почта"),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        max_length=150,
                        null=True,
                        verbose_name="имя пользователя",
                    ),
                ),
                (
                    "feedback",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="info",
                        related_query_name="info",
                        to="feedback.feedback",
                    ),
                ),
            ],
            options={
                "verbose_name": "данные пользователя",
                "verbose_name_plural": "много данных пользователя",
            },
        ),
        migrations.CreateModel(
            name="FeedbackFile",
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
                    "file",
                    models.FileField(
                        upload_to=feedback.models.FeedbackFile.create_path,
                        verbose_name="файлик",
                    ),
                ),
                (
                    "feedback",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        related_query_name="files",
                        to="feedback.feedback",
                    ),
                ),
            ],
            options={
                "verbose_name": "файлик фидбэка",
                "verbose_name_plural": "файлики фидбэка",
            },
        ),
    ]