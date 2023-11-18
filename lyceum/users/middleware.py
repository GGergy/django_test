from users.models import User


class UserProxyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, "user") and request.user.is_authenticated:
            request.user = User.objects.get(pk=request.user.pk)
        return self.get_response(request)


__all__ = []
