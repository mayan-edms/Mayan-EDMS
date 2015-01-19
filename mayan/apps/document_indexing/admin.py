from __future__ import unicode_literals

from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import Index, IndexInstanceNode, IndexTemplateNode


class IndexTemplateNodeAdmin(MPTTModelAdmin):
    list_display = ('expression', 'enabled', 'link_documents')


class IndexInstanceNodeAdmin(MPTTModelAdmin):
    model = IndexInstanceNode
    list_display = ('value',)


admin.site.register(Index)
admin.site.register(IndexTemplateNode, IndexTemplateNodeAdmin)
admin.site.register(IndexInstanceNode, IndexInstanceNodeAdmin)
