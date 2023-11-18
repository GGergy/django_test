from django.contrib import admin

import catalog.models


class ImagesInline(admin.StackedInline):
    model = catalog.models.ItemImage


class MainImageInline(admin.StackedInline):
    model = catalog.models.MainImage


@admin.register(catalog.models.Item)
class AdminItem(admin.ModelAdmin):
    inlines = [MainImageInline, ImagesInline]
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        "image_tmb",
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)
    readonly_fields = (
        catalog.models.Item.created_at.field.name,
        catalog.models.Item.updated_at.field.name,
    )


@admin.register(catalog.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = (catalog.models.Category.normalized_name.field.name,)


@admin.register(catalog.models.Tag)
class TagAdmin(admin.ModelAdmin):
    exclude = (catalog.models.Tag.normalized_name.field.name,)


__all__ = []
