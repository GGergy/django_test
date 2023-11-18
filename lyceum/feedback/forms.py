from django.forms import Form, ModelForm
from django.utils.translation import gettext_lazy as _

from core.forms import MultipleFileField
from feedback.models import Feedback, PersonalInfo


class FeedbackForm(
    ModelForm,
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Feedback
        fields = ("text",)
        labels = {
            "text": _("feedback_text"),
        }
        help_texts = {
            "text": _("feedback_text_help"),
        }
        exclude = ("created_on",)


class FeedbackInfoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = PersonalInfo
        fields = ("mail", "name")
        labels = {
            "mail": _("feedback_mail"),
            "name": _("feedback_name"),
        }
        help_texts = {
            "mail": _("feedback_mail_help"),
            "name": _("feedback_name_help"),
        }
        exclude = ("feedback",)


class FeedbackFileForm(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    files = MultipleFileField(
        label=_("feedback_file"),
        help_text=_("feedback_file_help"),
        required=False,
    )


__all__ = []
