from django.contrib.auth.models import User as DjangoUser, UserManager
from django.core.management import call_command
from django.db import models


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
    def get(self, *args, **kwargs):
        return (
            self.get_queryset().select_related("profile").get(*args, **kwargs)
        )

    def by_mail(self, mail):
        return self.get_queryset().get(email=mail)

    def users_list(self):
        return (
            self.get_queryset()
            .filter(is_active=True)
            .only(
                "username",
            )
            .select_related("profile")
        )

    def user_profile(self):
        return (
            self.get_queryset()
            .filter(is_active=True)
            .only("first_name", "last_name", "username")
            .select_related("profile")
        )


class User(DjangoUser):
    objects = MyUserManager()
    migrated = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.call_migrations()

    @classmethod
    def call_migrations(cls):
        if not cls.migrated:
            DjangoUser._meta.get_field("email")._unique = True
            call_command("makemigrations")
            call_command("migrate")
            cls.migrated = True

    def active(self):
        return self.is_active

    class Meta:
        proxy = True


__all__ = []
