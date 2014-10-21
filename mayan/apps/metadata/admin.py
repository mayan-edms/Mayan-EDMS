from __future__ import absolute_import

from django.contrib import admin

from .models import DocumentMetadata, DocumentTypeDefaults, MetadataType


class DocumentTypeDefaultsAdmin(admin.ModelAdmin):
    filter_horizontal = ('default_metadata',)


class MetadataTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'default', 'lookup')


class DocumentMetadataInline(admin.StackedInline):
    model = DocumentMetadata
    extra = 0
    classes = ('collapse-open',)
    allow_add = False


admin.site.register(DocumentTypeDefaults, DocumentTypeDefaultsAdmin)
admin.site.register(MetadataType, MetadataTypeAdmin)
