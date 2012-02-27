from __future__ import absolute_import

from django.contrib import admin

from .models import (MetadataType, MetadataSet, MetadataSetItem,
    DocumentMetadata, DocumentTypeDefaults)


class MetadataTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'default', 'lookup')


class MetadataSetItemInline(admin.StackedInline):
    model = MetadataSetItem
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class DocumentMetadataInline(admin.StackedInline):
    model = DocumentMetadata
    extra = 0
    classes = ('collapse-open',)
    allow_add = False


class MetadataSetAdmin(admin.ModelAdmin):
    inlines = [MetadataSetItemInline]


class DocumentTypeDefaultsAdmin(admin.ModelAdmin):
    filter_horizontal = ('default_metadata_sets', 'default_metadata')


admin.site.register(MetadataType, MetadataTypeAdmin)
admin.site.register(MetadataSet, MetadataSetAdmin)
admin.site.register(DocumentTypeDefaults, DocumentTypeDefaultsAdmin)
