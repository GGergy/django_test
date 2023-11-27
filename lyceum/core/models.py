from django.db import models
from sorl.thumbnail import get_thumbnail


class AbstractModel(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="название",
        help_text="Название элемента. Уникально для элементов одной модели",
        unique=True,
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="опубликовано",
        help_text="Показывает, будет ли элемент опубликован",
    )

    def __str__(self):
        return self.name[:15]

    class Meta:
        abstract = True


class AbstractImageModel(models.Model):
    image = models.ImageField(
        verbose_name="картинка",
        help_text="поле для загрузки изображения",
        upload_to="catalog/images/",
        default=None,
        blank=True,
    )

    def to_300x300(self):
        return get_thumbnail(self.image, "300x300", quality=51, crop='center')

    def as_path(self):
        return self.image.name

    def __str__(self):
        return self.image.name[:15]

    class Meta:
        abstract = True


__all__ = []
