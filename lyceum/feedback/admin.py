from django.contrib import admin

import feedback.models


class PersonalInfoInline(admin.StackedInline):
    model = feedback.models.PersonalInfo
    readonly_fields = (
        "name",
        "mail",
    )
    can_delete = False


class FilesInline(admin.StackedInline):
    model = feedback.models.FeedbackFile
    readonly_fields = ("file",)
    can_delete = False

    def has_add_permission(self, *args, **kwargs):
        return False


@admin.register(feedback.models.Feedback)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [PersonalInfoInline, FilesInline]
    list_display = ("text", "status")
    list_editable = ("status",)
    readonly_fields = (
        "text",
        "created_on",
    )
    exclude = ("user",)

    def save_model(self, request, obj, form, change):
        if "status" in form.changed_data:
            old_object = self.model.objects.filter(pk=obj.id).only("status")
            if old_object:
                feedback.models.StatusLog.objects.create(
                    to=obj.status,
                    user=request.user,
                    from_status=old_object[0].status,
                )
        super().save_model(request, obj, form, change)


__all__ = []
