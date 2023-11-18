from django.contrib.auth.backends import ModelBackend

from users.models import User


class MyAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        mail_user = self.by_mail(username)
        name_user = self.by_username(username)
        user = None
        if name_user:
            user = name_user
        elif mail_user:
            user = mail_user
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def by_mail(mail):
        try:
            return User.objects.by_mail(mail)
        except User.DoesNotExist:
            return False

    @staticmethod
    def by_username(username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return False


__all__ = []
