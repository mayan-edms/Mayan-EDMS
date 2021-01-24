from django.contrib import admin

from .models import DuplicateBackendEntry, StoredDuplicateBackend


@admin.register(DuplicateBackendEntry)
class DuplicateBackendEntryAdmin(admin.ModelAdmin):
    list_display = ('document',)


@admin.register(StoredDuplicateBackend)
class StoredDuplicateBackendAdmin(admin.ModelAdmin):
    list_display = (
        'backend_path', 'backend_data'
    )
