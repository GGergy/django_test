from django.db import models

from catalog.models import Item
from users.models import User


RATING_CHOICES = (
    ("1", "Ненависть"),
    ("2", "Неприязнь"),
    ("3", "Нейтрально"),
    ("4", "Обожание"),
    ("5", "Любовь"),
)


class ItemRating(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    rating = models.CharField(choices=RATING_CHOICES, max_length=10)
    created_at = models.DateTimeField(auto_now=True)


__all__ = []
