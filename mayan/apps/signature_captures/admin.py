from django.contrib import admin

from .models import SignatureCapture


@admin.register(SignatureCapture)
class SignatureCaptureAdmin(admin.ModelAdmin):
    list_display = (
        'document', 'internal_name', 'text', 'user', 'date_time_created',
        'date_time_edited'
    )
