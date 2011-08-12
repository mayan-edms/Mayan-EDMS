import os
import hashlib

from django.utils import simplejson
from django.http import HttpResponse
from django.template.defaultfilters import slugify

from documents.models import Document, DocumentType
from metadata.models import MetadataType, MetadataSet

FORMAT_VERSION = 1.0
HASH_FUNCTION = lambda x: hashlib.sha256(x).hexdigest()


def get_hash(obj):
    if obj:
        return u'%s_%s' % (HASH_FUNCTION(unicode(obj)), slugify(unicode(obj)))
    else:
        return None


'''


comments
tags
folders    

pages
pages transformation
metadata
doc_type metadata

sources
sources transform

users

class DocumentTypeDefaults(models.Model):
    """
    Default preselected metadata types and metadata set per document
    type
    """    
    document_type = models.ForeignKey(DocumentType, verbose_name=_(u'document type'))
    default_metadata_sets = models.ManyToManyField(MetadataSet, blank=True, verbose_name=_(u'default metadata sets'))
    default_metadata = models.ManyToManyField(MetadataType, blank=True, verbose_name=_(u'default metadata'))


'''

def export_test(request):
    big_list = []
    big_list.append({'version': FORMAT_VERSION})
    
    for metadata_type in MetadataType.objects.all():
        big_list.append(
            {
                'metadata_types': [
                    {
                        'id': get_hash(metadata_type.name),
                        'name': metadata_type.name,
                        'title': metadata_type.title,
                        'default': metadata_type.default,
                        'lookup': metadata_type.lookup,
                    }
                ]
            }
        )    

    for metadata_set in MetadataSet.objects.all():
        big_list.append(
            {
                'metadata_sets': [
                    {
                        'id': get_hash(metadata_set.title),
                        'name': metadata_set.title,
                        'metadata_types': [
                            {
                                'id': get_hash(metadata_type),
                            }
                            for metadata_type in metadata_set.metadatasetitem_set.all()
                        ]
                    }
                ]
            }
        )
    
    
    for document_type in DocumentType.objects.all():
        big_list.append(
            {
                'document_types': [
                    {
                        'id': get_hash(document_type.name),
                        'name': document_type.name,
                        'filenames': [
                            {
                                'filename': doc_type_filename.filename,
                                'enabled': doc_type_filename.enabled,
                            }
                            for doc_type_filename in document_type.documenttypefilename_set.all()
                        ],
                        'metadata_defaults': [
                            {
                                'default_metadata': [get_hash(metadata_type.name) for metadata_type in doc_type_defaults.default_metadata.all()],
                                'default_metadata_sets': [get_hash(metadata_set.title) for metadata_set in doc_type_defaults.default_metadata_sets.all()],
                            }
                            for doc_type_defaults in document_type.documenttypedefaults_set.all()
                        ]
                    }
                ]
            }
        )
    
    for document in Document.objects.all()[:10]:
        big_list.append(
            {
                'documents': [
                    {
                        'document_type': get_hash(document.document_type),
                        'filename': os.extsep.join([document.file_filename, document.file_extension]),
                        #'date_added'
                        'uuid': document.uuid,
                        'description': unicode(document.description) if document.description else None,
                        'tags': [get_hash(tag) for tag in document.tags.all()],
                        'folders': [get_hash(folder_document.folder) for folder_document in document.folderdocument_set.all()],
                        'comments': [
                            {
                                'comment': comment.comment,
                                'user': unicode(comment.user),
                                'submit_date': unicode(comment.submit_date),
                            }
                            for comment in document.comments.all()
                        ],
                        'versions': [
                            {
                                1.0: {
                                    'mimetype': document.file_mimetype,
                                    'encoding': document.file_mime_encoding,
                                    #'date_updated'
                                    'checksum': document.checksum,
                                }
                            }
                        ]
                    }
                ]
            }
        )
    
    return HttpResponse(simplejson.dumps(big_list, indent=4, ensure_ascii=True), mimetype='application/json')
