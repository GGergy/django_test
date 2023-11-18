from django import forms
from django.utils.translation import gettext_lazy as _


class CoffeeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    text = forms.CharField(
        help_text=_("echo_text_help"),
        label=_("echo_text_label"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )


__all__ = []
