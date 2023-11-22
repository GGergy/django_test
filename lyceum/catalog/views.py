from django.db.models import Avg
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy

from catalog.models import Item
from rating.forms import RatingForm
from rating.models import ItemRating


def item_list(request):
    data = Item.objects.published()
    return render(
        request,
        "catalog/item_list.html",
        context={"items": data},
    )


def friday(request):
    data = Item.objects.friday()
    return render(
        request,
        "catalog/3based.html",
        context={"items": data, "header": "friday"},
    )


def unverified(request):
    data = Item.objects.unverified()
    return render(
        request,
        "catalog/3based.html",
        context={"items": data, "header": "unverified"},
    )


def last_week(request):
    data = Item.objects.new()
    return render(
        request,
        "catalog/3based.html",
        context={"items": data, "header": "new"},
    )


def item_detail(request, item_id):
    item = Item.objects.full_item(item_id)
    item_ratings_middle = item.ratings.aggregate(Avg("rating")).get(
        "rating__avg",
    )
    if not item_ratings_middle:
        item_ratings_middle = gettext_lazy("no_rating")
    item_ratings_count = item.ratings.count()
    form = None
    if request.user.is_authenticated:
        rating = item.ratings.filter(user=request.user).first()
        form = RatingForm(request.POST or None, instance=rating)
        if request.method == "POST" and form.is_valid():
            if rating:
                form.save()
            else:
                ItemRating.objects.create(
                    user=request.user,
                    item=item,
                    rating=form.cleaned_data["rating"],
                )
            return redirect("catalog:item_detail_site", item_id=item_id)
    return render(
        request,
        "catalog/item.html",
        context={
            "item": item,
            "item_ratings_count": item_ratings_count,
            "item_ratings_middle": item_ratings_middle,
            "form": form,
        },
    )


__all__ = []
