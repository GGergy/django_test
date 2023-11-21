from datetime import datetime

from users.models import Profile


def birthday_users(request):
    userDate = request.COOKIES.get('userDate')
    user_y, user_m, user_d = str(userDate).split("-")

    if userDate:
        matching_users = Profile.objects.filter(
            birthday__month=user_m,
            birthday__day=user_d,
        )

    return {
        "userDate": userDate,
        'birthday_users': matching_users,
    }
