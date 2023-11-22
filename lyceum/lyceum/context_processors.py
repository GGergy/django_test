from datetime import datetime

from users.models import Profile


def birthday_users(request):
    userdate = request.COOKIES.get("userDate")
    if not userdate:
        userdate = datetime.now().date()
    user_y, user_m, user_d = str(userdate).split("-")

    if userdate:
        matching_users = Profile.objects.filter(
            birthday__month=user_m,
            birthday__day=user_d,
        )

    return {
        "userDate": userdate,
        "birthday_users": matching_users,
    }


__all__ = []
