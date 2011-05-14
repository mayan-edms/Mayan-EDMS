from django.contrib import admin

from document_indexing.models import DocumentIndex

#from filesystem_serving.admin import DocumentMetadataIndexInline


#class MetadataIndexInline(admin.StackedInline):
#    model = MetadataIndex
#    extra = 1
#    classes = ('collapse-open',)
#    allow_add = True


class DocumentIndexAdmin(admin.ModelAdmin):
    pass
    #inlines = [
    #    DocumentMetadataIndexInline,
    #



admin.site.register(DocumentIndex, DocumentIndexAdmin)
