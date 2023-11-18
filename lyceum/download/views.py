from django.conf import settings
from django.http import FileResponse, Http404


def download_pic(request, path):
    file_path = settings.MEDIA_ROOT / path
    if file_path.exists():
        return FileResponse(open(file_path, "rb"), as_attachment=True)
    raise Http404


__all__ = []
