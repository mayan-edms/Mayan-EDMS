from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    filter_horizontal = ('documents',)
    list_display = ('label', 'color', 'get_preview_widget')
