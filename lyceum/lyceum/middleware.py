import re

from django.conf import settings


class TeapotMiddleware:
    counter = 0

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def change_counter(cls):
        cls.counter += 1

    def __call__(self, request):
        self.change_counter()
        response = self.get_response(request)

        if not settings.ALLOW_REVERSE:
            return response

        if self.counter % 10 == 0:
            content = response.content.decode()
            content = re.sub(
                r"\b[А-ЯЁа-яё]+\b",
                lambda match: match.group()[::-1],
                content,
            )
            response.content = content.encode()

        return response


__all__ = []
