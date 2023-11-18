from django.conf import settings
from django.db import models


RECEIVED = "получено"
PROCESSING = "в обработке"
ANSWERED = "ответ дан"
STATUS_CHOICES = (
    (RECEIVED, "получено"),
    (PROCESSING, "в обработке"),
    (ANSWERED, "ответ дан"),
)


class Feedback(models.Model):
    text = models.TextField(verbose_name="текст сообщения")
    created_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата создания",
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default=RECEIVED,
        verbose_name="статус вопроса",
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = "фидбэк"
        verbose_name_plural = "фидбэки"


class FeedbackFile(models.Model):
    def create_path(self, filename, **kwargs):
        return f"uploads/{self.feedback_id}/{filename}"

    file = models.FileField(upload_to=create_path, verbose_name="файлик")
    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        related_query_name="files",
        related_name="files",
    )

    def __str__(self):
        return self.file.name[:15]

    class Meta:
        verbose_name = "файлик фидбэка"
        verbose_name_plural = "файлики фидбэка"


class PersonalInfo(models.Model):
    feedback = models.OneToOneField(
        Feedback,
        on_delete=models.CASCADE,
        related_query_name="info",
        related_name="info",
    )
    mail = models.EmailField(verbose_name="почта")
    name = models.CharField(
        max_length=150,
        verbose_name="имя пользователя",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.mail[:15]

    class Meta:
        verbose_name = "данные пользователя"
        verbose_name_plural = "много данных пользователя"


class StatusLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )
    from_status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        db_column="from",
    )
    to = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
    )


__all__ = []
