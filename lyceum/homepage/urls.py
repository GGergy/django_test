from django.urls import path

from homepage import views


app_name = "homepage"


urlpatterns = [
    path("", views.home, name="main"),
    path("coffee/", views.coffee, name="coffee"),
    path("echo/", views.echo, name="echo"),
    path("echo/submit/", views.echo_submit, name="echo_submit"),
    path("user_list/", views.user_list, name="user_list"),
    path(
        "user_detail/<int:user_id>/",
        views.user_detail,
        name="user_detail",
    ),
]


__all__ = []
