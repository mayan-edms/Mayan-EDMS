from django.contrib import admin

from models import MetadataType, DocumentType, Document, \
    DocumentTypeMetadataType, DocumentMetadata


class MetadataTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'default', 'lookup')
        
    
class DocumentTypeMetadataTypeInline(admin.StackedInline):
    model = DocumentTypeMetadataType
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class DocumentTypeAdmin(admin.ModelAdmin):
    inlines = [DocumentTypeMetadataTypeInline]


class DocumentMetadataInline(admin.StackedInline):
    model = DocumentMetadata
    extra = 1
    classes = ('collapse-open',)
    allow_add = True    


class DocumentAdmin(admin.ModelAdmin):
    inlines = [DocumentMetadataInline,]
    list_display = ('uuid', 'file_filename', 'file_extension', 'file_mimetype')


admin.site.register(MetadataType, MetadataTypeAdmin)
admin.site.register(DocumentType, DocumentTypeAdmin)
admin.site.register(Document, DocumentAdmin)
                
