from django.core.urlresolvers import reverse

from djangorestframework.resources import ModelResource

from documents.models import Document
from converter.exceptions import UnknownFileFormat, UnkownConvertError


class DocumentResourceSimple(ModelResource):
    model = Document
    fields = ('url', 'pk', 'document_type', 'uuid', 'date_added', 'description', 'tags', 'comments', 'expensive_methods', 'files')
   
    def files(self, instance):
        return [
            {
                'version': 1,
                'mimetype': instance.file_mimetype,
                'encoding': instance.file_mime_encoding,
                'filename': instance.get_fullname(),
                'date_updated': instance.date_updated,
                'checksum': instance.checksum,
                'size': instance.size,
                'exists': instance.exists(),
                'pages': [
                    {
                        'page_numer': page.page_number,
                        'page_label': page.page_label,
                        'is_zoomable': reverse('documents-expensive-is_zoomable', args=[instance.pk, page.page_number]),
                        
                        #'content':
                    }
                    for page in instance.documentpage_set.all()
                ]
            }
        ]
    
    def expensive_methods(self, instance):
        return []
