from datetime import datetime
from datetime import timedelta

from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.safestring import mark_safe

from catalog.validators import (
    ValidateMustContain,
    ValidateNormalizedNameByClass,
)
from core.models import AbstractImageModel, AbstractModel


class ItemManager(models.Manager):
    def published(self):
        return (
            self.get_queryset()
            .filter(is_published=True)
            .select_related("category")
            .filter(category__is_published=True)
            .order_by("category__name")
            .prefetch_related(
                models.Prefetch(
                    "tags",
                    queryset=Tag.objects.filter(is_published=True).only(
                        "name",
                    ),
                ),
            )
            .only("name", "text", "category__name")
        )

    def on_main(self):
        return (
            self.get_queryset()
            .filter(is_published=True, is_on_main=True)
            .select_related("category")
            .filter(category__is_published=True)
            .order_by("name")
            .prefetch_related(
                models.Prefetch(
                    "tags",
                    queryset=Tag.objects.filter(is_published=True).only(
                        "name",
                    ),
                ),
            )
            .only("name", "text", "category__name")
        )

    def full_item(self, pk):
        return get_object_or_404(
            self.get_queryset()
            .filter(is_published=True)
            .select_related("category")
            .filter(category__is_published=True)
            .prefetch_related(
                models.Prefetch(
                    "tags",
                    queryset=Tag.objects.filter(is_published=True).only(
                        "name",
                    ),
                ),
            )
            .select_related("main_image")
            .prefetch_related("images")
            .only(
                "name",
                "text",
                "category__name",
                "main_image__image",
                "ratings",
            ),
            pk=pk,
        )

    def friday(self):
        return (
            self.published()
            .filter(updated_at__iso_week_day=5)
            .order_by("updated_at")[:5]
        )

    def new(self):
        now_date = timezone.make_aware(
            datetime.now(),
            timezone.get_current_timezone(),
        )
        return (
            self.published()
            .filter(
                created_at__range=[
                    now_date - timedelta(days=7),
                    now_date,
                ],
            )
            .order_by("?")[:5]
        )

    def unverified(self):
        return self.published().filter(
            created_at__range=[
                models.F("updated_at") - timedelta(seconds=1),
                models.F("updated_at") + timedelta(seconds=1),
            ],
        )


class Tag(AbstractModel):
    slug = models.SlugField(
        max_length=200,
        verbose_name="слаг",
        help_text=(
            "Слаг элемента. Уникален для каждой категории. "
            "Содержит только символы латиницы, цифры и символы `-_`"
        ),
        unique=True,
    )

    normalized_name = models.CharField(
        max_length=150,
        verbose_name="нормализованное имя",
        help_text="ты не должен это видеть",
        default=None,
        null=True,
    )

    def full_clean(self, *args, **kwargs):
        self.normalized_name = ValidateNormalizedNameByClass(Tag, self.id)(
            self.name,
        )
        super().full_clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.normalized_name:
            self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"


class Category(AbstractModel):
    weight = models.IntegerField(
        verbose_name="Вес",
        default=100,
        validators=[MinValueValidator(1), MaxValueValidator(32768)],
        help_text="Вес категории. Имеет значение от 0 до 32767",
    )

    slug = models.SlugField(
        max_length=200,
        verbose_name="слаг",
        help_text=(
            "Слаг элемента. Уникален для каждой категории. "
            "Содержит только символы латиницы, цифры и символы `-_`"
        ),
        unique=True,
    )

    normalized_name = models.CharField(
        max_length=150,
        verbose_name="нормализованное имя",
        help_text="ты не должен это видеть",
        default=None,
        null=True,
    )

    def full_clean(self, *args, **kwargs):
        self.normalized_name = ValidateNormalizedNameByClass(
            Category,
            self.id,
        )(self.name)
        super().full_clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.normalized_name:
            self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Item(AbstractModel):
    objects = ItemManager()

    text = RichTextUploadingField(
        verbose_name="текст",
        validators=[ValidateMustContain("превосходно", "роскошно")],
        help_text="Описание товара."
        " Обязательно содержит слова `Роскошно` или `Превосходно`",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="категория",
        help_text="Категория товара. Одна из списка созданных категорий",
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="items",
        help_text="Теги товара. Их может быть сколько угодно, но хотя бы один",
        verbose_name="теги",
    )

    is_on_main = models.BooleanField(
        default=False,
        verbose_name="опубликовано на главной",
        help_text="Отображать элемент на главной странице?",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="создан",
        null=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="обновлен",
        null=True,
    )

    def image_tmb(self):
        if self.main_image.image:
            return mark_safe(
                f'<img src="{self.main_image.image.url}" width="50">',
            )
        return "Нет изображения"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"


class ItemImage(AbstractImageModel):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_query_name="images",
        related_name="images",
    )

    class Meta:
        verbose_name = "картинка товара"
        verbose_name_plural = "картинки товара"


class MainImage(AbstractImageModel):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        related_query_name="main_image",
        related_name="main_image",
    )

    class Meta:
        verbose_name = "главная картинка товара"
        verbose_name_plural = "главные картинки товара"


__all__ = []
