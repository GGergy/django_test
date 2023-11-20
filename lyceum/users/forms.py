from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


from users.models import Profile, User


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class UserUpdateForm(UserChangeForm):
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(UserChangeForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )


class UpdateProfileForm(
    forms.ModelForm,
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["coffee_count"].widget.attrs.update(
            {"disabled": "disabled"},
        )
        self.fields["coffee_count"].required = False
        self.fields["birthday"].widget = forms.SelectDateWidget(
            attrs={"class": "form-control"},
            years=range(1900, datetime.now().year + 1),
        )
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Profile
        fields = (
            Profile.image.field.name,
            Profile.birthday.field.name,
            Profile.coffee_count.field.name,
        )


__all__ = []
