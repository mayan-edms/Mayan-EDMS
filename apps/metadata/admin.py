from django.contrib import admin

from metadata.models import MetadataType, MetadataSet, MetadataSetItem, \
    DocumentMetadata


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


admin.site.register(MetadataType, MetadataTypeAdmin)
admin.site.register(MetadataSet, MetadataSetAdmin)
