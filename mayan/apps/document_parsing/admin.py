from django.contrib import admin

from .models import DocumentFilePageContent


@admin.register(DocumentFilePageContent)
class DocumentFilePageContentAdmin(admin.ModelAdmin):
    list_display = ('document_file_page',)
