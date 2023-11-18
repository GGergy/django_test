from http import HTTPStatus

from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Item
from homepage.forms import CoffeeForm
from users.models import User


def home(request):
    items = Item.objects.on_main()
    return render(request, "homepage/home.html", context={"items": items})


def coffee(request):
    if hasattr(request.user, "profile"):
        request.user.profile.coffee_count += 1
        request.user.profile.save()
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


def echo(request):
    if request.method == "GET":
        form = CoffeeForm()
        return render(request, "homepage/echo.html", {"form": form})
    return HttpResponseNotAllowed(permitted_methods=["GET"])


def echo_submit(request):
    if request.method == "POST":
        form = CoffeeForm(request.POST or None)
        if form.is_valid():
            return HttpResponse(form.cleaned_data["text"])
        return redirect("homepage:echo")
    return HttpResponseNotAllowed(permitted_methods=["POST"])


def user_list(request):
    users = User.objects.users_list()
    return render(request, "users/user_list.html", {"users": users})


def user_detail(request, user_id):
    user = get_object_or_404(
        User.objects.user_profile(),
        pk=user_id,
    )
    return render(request, "users/user_detail.html", {"user": user})


__all__ = []
