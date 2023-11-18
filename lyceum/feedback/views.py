from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy

from feedback.forms import FeedbackFileForm, FeedbackForm, FeedbackInfoForm
from feedback.models import FeedbackFile, PersonalInfo


def feedback(request):
    form = FeedbackForm(request.POST or None)
    info_form = FeedbackInfoForm(request.POST or None)
    file_form = FeedbackFileForm(request.POST or None, request.FILES or None)
    if (
        request.method == "POST"
        and form.is_valid()
        and info_form.is_valid()
        and file_form.is_valid()
    ):
        send_mail(
            subject="feedback",
            message=form.cleaned_data["text"],
            from_email=settings.DJANGO_MAIL,
            recipient_list=[info_form.cleaned_data["mail"]],
        )
        instanse = form.save().pk
        info_object = PersonalInfo(
            mail=info_form.cleaned_data["mail"],
            name=info_form.cleaned_data["name"],
            feedback_id=instanse,
        )
        info_object.save()
        for file in request.FILES.getlist("files"):
            file_object = FeedbackFile(file=file, feedback_id=instanse)
            file_object.save()
        messages.success(
            request,
            gettext_lazy("form_success")
            + f" ({form.cleaned_data['text'][:30]}...)",
        )
        return redirect("feedback:feedback")
    return render(
        request,
        "feedback/feedback.html",
        {"form": form, "info_form": info_form, "file_form": file_form},
    )


__all__ = []
