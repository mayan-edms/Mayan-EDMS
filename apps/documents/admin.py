from django.contrib import admin

from models import MetadataType, DocumentType, Document, \
    DocumentTypeMetadataTypeConnector

admin.site.register(MetadataType)
admin.site.register(DocumentType)
admin.site.register(Document)
admin.site.register(DocumentTypeMetadataTypeConnector)
                         
