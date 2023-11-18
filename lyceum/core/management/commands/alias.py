import os
import pathlib
import shutil
import sys

from decouple import config
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command

from core.management.commands.boot import SimpleCommand


class MakeApplyMigrationsCommand(SimpleCommand):
    priority = 2
    verbose_name = "Создание и запуск миграций"

    @staticmethod
    def add_arguments(parser):
        parser.add_argument("-na", "--no-apply", action="store_true")

    @staticmethod
    def run(handler, **kwargs):
        call_command(
            "makemigrations",
        )
        if not kwargs["no_apply"]:
            call_command(
                "migrate",
            )


class CreateAdminCommand(SimpleCommand):
    verbose_name = "Создание админа"

    @staticmethod
    def get_password():
        if config("ADMIN_PASSWORD", default=None):
            return config("ADMIN_PASSWORD")
        return input("Set admin password: ")

    @staticmethod
    def add_arguments(parser):
        parser.add_argument("-u", "--username", default="default")

    def run(self, handler, **kwargs):
        if User.objects.count() > 0:
            handler.stdout.write("Cannot create admin. Admin already exist")
            return
        user = User(
            is_staff=True,
            is_superuser=True,
            username=kwargs.get("username"),
            email=settings.DJANGO_MAIL,
        )
        user.set_password(self.get_password())
        user.save()
        handler.stdout.write(f"Successfully created admin {user.username}")


class LoadFixturesCommand(SimpleCommand):
    verbose_name = "Загрузка меню и фикстур"

    @staticmethod
    def add_arguments(parser):
        parser.add_argument("-nm", "--no_media", action="store_true")

    @staticmethod
    def run(handler, **kwargs):
        if not kwargs.get("no_media"):
            if pathlib.Path("media/").is_dir():
                handler.stdout.write(
                    "Cannot create media directory, it's already exist",
                )
            else:
                shutil.copytree(src="fixtures/media", dst="media")
                handler.stdout.write("Finish copying media directory")
        call_command(
            "loaddata",
            "fixtures/data.json",
        )
        handler.stdout.write("Finish loading fixtures")


class CompileMessagesCommand(SimpleCommand):
    verbose_name = "Компиляция языковых пакетов"

    @staticmethod
    def run(handler, **kwargs):
        call_command(
            "compilemessages",
        )


class ClearThumbnailCommand(SimpleCommand):
    verbose_name = "Очистка кэша thumbnail"

    @staticmethod
    def run(handler, **kwargs):
        os.system(f"{sys.executable} manage.py thumbnail clear")


class InstallRequirementsCommand(SimpleCommand):
    priority = 1
    verbose_name = "Установка зависимостей"

    @staticmethod
    def add_arguments(parser):
        parser.add_argument("-d", "--dev", action="store_true")
        parser.add_argument("-p", "--prod", action="store_true")

    @staticmethod
    def run(handler, **kwargs):
        if kwargs["dev"]:
            os.system("pip install -r ../requirements/dev.txt")
        if kwargs["prod"]:
            os.system("pip install -r ../requirements/prod.txt")


class RenameEnvCommand(SimpleCommand):
    priority = 0
    verbose_name = "Переименование файла test.env"

    @staticmethod
    def run(handler, **kwargs):
        if pathlib.Path("../.env").exists():
            handler.stdout.write(".env file already exists")
            return
        pathlib.Path("../test.env").rename("../.env")


__all__ = []
