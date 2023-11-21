from django.db.models import Avg
from django.shortcuts import render
from django.views import generic

from catalog.models import Item
from rating.models import ItemRating


class BestWorstView(generic.View):
    template_name = "statistic/best-worst.html"

    def get(self, request, *args, **kwargs):
        try:
            best_item = (
                ItemRating.objects.filter(user=request.user)
                .select_related("item")
                .only("item__name", "rating", "created_at")
                .order_by("-rating", "-created_at")
                .first()
            )
            worst_item = (
                ItemRating.objects.filter(user=request.user)
                .select_related("item")
                .only("item__name", "rating", "created_at")
                .order_by("rating", "-created_at")
                .first()
            )
        except Exception:
            best_item = None
            worst_item = None
        rating_counts = ItemRating.objects.filter(user=request.user).count()
        rating_middle = (
            ItemRating.objects.filter(user=request.user)
            .aggregate(Avg("rating"))
            .get("rating__avg")
        )
        if not rating_middle:
            rating_middle = "Нет"
        return render(
            request,
            self.template_name,
            {
                "best_item": best_item,
                "worst_item": worst_item,
                "rating_counts": rating_counts,
                "rating_middle": rating_middle,
            },
        )


class RatedListView(generic.ListView):
    template_name = "statistic/rated-list.html"

    def get(self, request, *args, **kwargs):
        rated_items = (
            ItemRating.objects.filter(user=request.user)
            .select_related("item")
            .only("item__name", "rating", "created_at")
            .order_by("-rating")
        )
        return render(request, self.template_name, {"items": rated_items})


class ItemRatingInfoView(generic.ListView):
    template_name = "statistic/item-rating-info.html"

    def get(self, request, *args, **kwargs):
        items = (
            Item.objects.select_related("main_image")
            .only("name", "main_image__image")
            .all()
        )
        answer = []
        for item in items:
            queryset = ItemRating.objects.filter(item=item)
            rating_counts = queryset.count()
            rating_middle = queryset.aggregate(Avg("rating")).get(
                "rating__avg",
            )
            if not rating_middle:
                rating_middle = "Нет"
            last_bad = (
                queryset.select_related("user")
                .order_by("rating", "-created_at")
                .values("user__username", "rating")
                .first()
            )
            last_good = (
                queryset.select_related("user")
                .order_by("-rating", "-created_at")
                .values("user__username", "rating")
                .first()
            )
            answer.append(
                {
                    "item": item,
                    "rating_counts": rating_counts,
                    "rating_middle": rating_middle,
                    "last_bad": last_bad,
                    "last_good": last_good,
                },
            )
        return render(request, self.template_name, context={"items": answer})


__all__ = []
