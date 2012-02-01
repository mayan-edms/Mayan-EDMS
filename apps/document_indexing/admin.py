from __future__ import absolute_import

from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import (Index, IndexTemplateNode, IndexInstanceNode,
    DocumentRenameCount)


#class IndexInstanceInline(admin.StackedInline):
#    model = IndexInstance
#    extra = 1#
#    classes = ('collapse-open',)
#    allow_add = True


class IndexTemplateNodeAdmin(MPTTModelAdmin):
    list_display = ('expression', 'enabled', 'link_documents')


class IndexInstanceNodeAdmin(MPTTModelAdmin):
    model = IndexInstanceNode
    list_display = ('value',)# 'get_document_list_display')


admin.site.register(Index)
admin.site.register(IndexTemplateNode, IndexTemplateNodeAdmin)
admin.site.register(IndexInstanceNode, IndexInstanceNodeAdmin)
admin.site.register(DocumentRenameCount)
