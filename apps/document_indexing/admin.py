from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from document_indexing.models import Index, IndexInstance, \
    DocumentRenameCount


class IndexInstanceInline(admin.StackedInline):
    model = IndexInstance
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class IndexAdmin(MPTTModelAdmin):
    list_display = ('expression', 'enabled', 'link_documents')
    
    
class IndexInstanceAdmin(MPTTModelAdmin):
    model = IndexInstance
    list_display = ('value', 'index', 'get_document_list_display')


admin.site.register(Index, IndexAdmin)
admin.site.register(IndexInstance, IndexInstanceAdmin)
admin.site.register(DocumentRenameCount)
