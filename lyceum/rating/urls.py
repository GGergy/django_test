from django.urls import path

from rating import views


app_name = "rating"


urlpatterns = [
    path(
        "delete_rating/<int:item_id>",
        views.DeleteRatingView.as_view(),
        name="delete_rating",
    ),
]


__all__ = []
