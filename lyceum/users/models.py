import sys

from django.contrib.auth.models import User as DjangoUser, UserManager
from django.db import models


if {"makekigrations", "migrate"}.intersection(set(sys.argv)) == {}:
    DjangoUser._meta.get_field("email")._unique = True


class Profile(models.Model):
    user = models.OneToOneField(
        DjangoUser,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    birthday = models.DateField(null=True, blank=True)
    image = models.ImageField(
        upload_to="uploads/profile_pics/",
        null=True,
        blank=True,
    )
    coffee_count = models.PositiveIntegerField(default=0)


class MyUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().select_related("profile")

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def by_mail(self, mail):
        return self.active().get(email=mail)


class User(DjangoUser):
    objects = MyUserManager()

    class Meta:
        proxy = True


__all__ = []
