from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Index, IndexInstanceNode, IndexTemplateNode


class IndexTemplateNodeInline(admin.StackedInline):
    extra = 0
    list_display = ('expression', 'enabled', 'link_documents')
    model = IndexTemplateNode


class IndexAdmin(admin.ModelAdmin):
    filter_horizontal = ('document_types',)
    inlines = [IndexTemplateNodeInline]
    list_display = ('name', 'title', 'enabled', 'get_document_types')

    def get_document_types(self, instance):
        return ', '.join(['"{0}"'.format(document_type) for document_type in instance.document_types.all()]) or _('None')

    get_document_types.short_description = _('Document types')


admin.site.register(Index, IndexAdmin)



