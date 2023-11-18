from django.urls import re_path

from download import views


app_name = "download"


urlpatterns = [
    re_path(r"(?P<path>.*)", views.download_pic, name="main"),
]


__all__ = []
