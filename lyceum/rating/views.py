from django.http import HttpResponseNotAllowed
from django.views import generic
from django.shortcuts import redirect

from rating.models import ItemRating


class DeleteRatingView(generic.View):
    def post(self, request, item_id, *args, **kwargs):
        rating = ItemRating.objects.filter(
            user=request.user, item_id=item_id
        ).first()
        if rating:
            rating.delete()
        return redirect("catalog:item_detail_site", item_id=item_id)

    def get(self, request, item_id, *args, **kwargs):
        return HttpResponseNotAllowed("POST")
