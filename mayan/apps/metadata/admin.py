from __future__ import absolute_import

from django.contrib import admin

from .models import (DocumentMetadata, DocumentTypeDefaults, MetadataSet,
                     MetadataSetItem, MetadataType)


class DocumentTypeDefaultsAdmin(admin.ModelAdmin):
    filter_horizontal = ('default_metadata_sets', 'default_metadata')


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


admin.site.register(DocumentTypeDefaults, DocumentTypeDefaultsAdmin)
admin.site.register(MetadataSet, MetadataSetAdmin)
admin.site.register(MetadataType, MetadataTypeAdmin)
