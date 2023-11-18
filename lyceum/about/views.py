from django.shortcuts import render


def description(request):
    return render(
        request,
        "about/about.html",
    )


__all__ = []
