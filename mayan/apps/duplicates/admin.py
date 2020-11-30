from django.contrib import admin

from .models import DuplicatedDocument


@admin.register(DuplicatedDocument)
class DuplicatedDocumentAdmin(admin.ModelAdmin):
    list_display = (
        'document', 'datetime_added'
    )
