from django.urls import path

from catalog import views


app_name = "catalog"


urlpatterns = [
    path("", views.item_list, name="main"),
    path("<int:item_id>/", views.item_detail, name="item_detail_site"),
    path("new/", views.last_week, name="new"),
    path("friday/", views.friday, name="friday"),
    path("unverified/", views.unverified, name="unverified"),
]


__all__ = []
