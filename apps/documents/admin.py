from django.contrib import admin

from models import MetadataType, DocumentType, Document, \
    DocumentTypeMetadataType, DocumentMetadata, DocumentTypeFilename#, \
#    DocumentFile


class MetadataTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'default', 'lookup')
        
    
class DocumentTypeMetadataTypeInline(admin.StackedInline):
    model = DocumentTypeMetadataType
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class DocumentTypeFilenameInline(admin.StackedInline):
    model = DocumentTypeFilename
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class DocumentTypeAdmin(admin.ModelAdmin):
    inlines = [DocumentTypeMetadataTypeInline, DocumentTypeFilenameInline]


class DocumentMetadataInline(admin.StackedInline):
    model = DocumentMetadata
    extra = 1
    classes = ('collapse-open',)
    allow_add = True    


#class DocumentFileInline(admin.StackedInline):
#    model = DocumentFile
#    extra = 1
#    classes = ('collapse-open',)
#    allow_add = True    


class DocumentAdmin(admin.ModelAdmin):
    #inlines = [DocumentFileInline]#, DocumentMetadataInline,]
    inlines = [DocumentMetadataInline]
    list_display = ('uuid',)
    
    



admin.site.register(MetadataType, MetadataTypeAdmin)
admin.site.register(DocumentType, DocumentTypeAdmin)
admin.site.register(Document, DocumentAdmin)
                
