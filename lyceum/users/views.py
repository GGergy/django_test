import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from users.forms import SignUpForm, UpdateProfileForm, UserUpdateForm
from users.models import Profile


def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        instance = form.save()
        Profile.objects.create(user=instance)
        if settings.DEFAULT_USER_IS_ACTIVE and "email" in form.cleaned_data:
            invite_link = request.build_absolute_uri(
                reverse(
                    "users:activate",
                    args=[
                        TimestampSigner().sign(form.cleaned_data["username"]),
                    ],
                ),
            )
            send_mail(
                subject="Verification email",
                message=f"Welcome! For activate your account,"
                f" go to:\n{invite_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[form.cleaned_data["email"]],
            )
        messages.success(
            request,
            "Your account created successfully, check your email"
            " for more information",
        )
        return redirect(reverse("homepage:main"))
    return render(
        request,
        "users/signup.html",
        {"form": form},
    )


def activate(request, username):
    username = TimestampSigner().unsign(
        username,
        max_age=datetime.timedelta(hours=12),
    )
    user = User.objects.get(username=username)
    if timezone.now() - user.date_joined < datetime.timedelta(hours=12):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated!")
    else:
        messages.warning(
            request,
            "Couldn't activate your account, it's over 12 hours ago",
        )
    return redirect(reverse("homepage:main"))


@login_required(login_url=reverse_lazy("users:login"))
def update_profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile,
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile is updated successfully")
            return redirect(reverse("users:profile"))
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(
        request,
        "users/profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


__all__ = []
