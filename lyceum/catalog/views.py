from django.shortcuts import render

from catalog.models import Item


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
    return render(
        request,
        "catalog/item.html",
        context={
            "item": item,
        },
    )


__all__ = []
