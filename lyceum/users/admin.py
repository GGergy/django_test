from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminModel
from django.contrib.auth.models import User

from users.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    readonly_fields = ("coffee_count",)
    can_delete = False


class UserAdmin(UserAdminModel):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


__all__ = []
