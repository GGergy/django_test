from django.forms import ModelForm
from django.utils.translation import gettext_lazy

from rating.models import ItemRating


class RatingForm(ModelForm):

    class Meta:
        model = ItemRating
        fields = ("rating",)
        labels = {"rating": gettext_lazy('rating')}
