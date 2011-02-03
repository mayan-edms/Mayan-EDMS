from django.contrib import admin

from models import MetadataType, DocumentType, Document, \
    DocumentTypeMetadataType, DocumentMetadata

admin.site.register(MetadataType)
admin.site.register(DocumentType)
admin.site.register(Document)
admin.site.register(DocumentTypeMetadataType)
admin.site.register(DocumentMetadata)
                         
