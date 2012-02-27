from __future__ import absolute_import

from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import (Index, IndexTemplateNode, IndexInstanceNode,
    DocumentRenameCount)


class IndexTemplateNodeAdmin(MPTTModelAdmin):
    list_display = ('expression', 'enabled', 'link_documents')


class IndexInstanceNodeAdmin(MPTTModelAdmin):
    model = IndexInstanceNode
    list_display = ('value',)


admin.site.register(Index)
admin.site.register(IndexTemplateNode, IndexTemplateNodeAdmin)
admin.site.register(IndexInstanceNode, IndexInstanceNodeAdmin)
admin.site.register(DocumentRenameCount)
