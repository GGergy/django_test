from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy

from statistic import views


app_name = "statistic"


urlpatterns = [
    path(
        "best_worst",
        login_required(
            views.BestWorstView.as_view(),
            login_url=reverse_lazy("users:login"),
        ),
        name="best_worst",
    ),
    path(
        "rated_list",
        login_required(
            views.RatedListView.as_view(),
            login_url=reverse_lazy("users:login"),
        ),
        name="rated_list",
    ),
    path(
        "item_rating_info",
        views.ItemRatingInfoView.as_view(),
        name="item_rating_info",
    ),
]


__all__ = []
