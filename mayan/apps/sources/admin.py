from django.contrib import admin

from .models import Source


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('label', 'enabled', 'backend_path', 'backend_data')
