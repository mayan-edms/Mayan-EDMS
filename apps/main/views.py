import os
import types

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from common.conf import settings as common_settings
from documents.conf import settings as documents_settings
from converter.conf import settings as converter_settings
from ocr.conf import settings as ocr_settings
from filesystem_serving.conf import settings as filesystem_serving_settings


def home(request):
    return render_to_response('home.html', {},
    context_instance=RequestContext(request))

def check_settings(request):
    settings = [
        {'name':'DOCUMENTS_METADATA_AVAILABLE_FUNCTIONS', 'value':documents_settings.AVAILABLE_FUNCTIONS},
        {'name':'DOCUMENTS_METADATA_AVAILABLE_MODELS', 'value':documents_settings.AVAILABLE_MODELS},
        {'name':'DOCUMENTS_USE_STAGING_DIRECTORY', 'value':documents_settings.USE_STAGING_DIRECTORY},
        {'name':'DOCUMENTS_STAGING_DIRECTORY', 'value':documents_settings.STAGING_DIRECTORY, 'exists':True},
        {'name':'DOCUMENTS_DELETE_STAGING_FILE_AFTER_UPLOAD', 'value':documents_settings.DELETE_STAGING_FILE_AFTER_UPLOAD},
        {'name':'DOCUMENTS_STAGING_FILES_PREVIEW_SIZE', 'value':documents_settings.STAGING_FILES_PREVIEW_SIZE},
        {'name':'DOCUMENTS_CHECKSUM_FUNCTION', 'value':documents_settings.CHECKSUM_FUNCTION},
        {'name':'DOCUMENTS_UUID_FUNTION', 'value':documents_settings.UUID_FUNCTION},
        {'name':'DOCUMENTS_STORAGE_BACKEND', 'value':documents_settings.STORAGE_BACKEND},
        {'name':'DOCUMENTS_STORAGE_DIRECTORY_NAME', 'value':documents_settings.STORAGE_DIRECTORY_NAME},
        {'name':'DOCUMENTS_PREVIEW_SIZE', 'value':documents_settings.PREVIEW_SIZE},
        {'name':'DOCUMENTS_THUMBNAIL_SIZE', 'value':documents_settings.THUMBNAIL_SIZE},
        {'name':'DOCUMENTS_DISPLAY_SIZE', 'value':documents_settings.DISPLAY_SIZE},
        {'name':'DOCUMENTS_AUTOMATIC_OCR', 'value':documents_settings.AUTOMATIC_OCR},
        {'name':'DOCUMENTS_ENABLE_SINGLE_DOCUMENT_UPLOAD', 'value':documents_settings.ENABLE_SINGLE_DOCUMENT_UPLOAD},
        {'name':'DOCUMENTS_UNCOMPRESS_COMPRESSED_LOCAL_FILES', 'value':documents_settings.UNCOMPRESS_COMPRESSED_LOCAL_FILES},
        {'name':'DOCUMENTS_UNCOMPRESS_COMPRESSED_STAGING_FILES', 'value':documents_settings.UNCOMPRESS_COMPRESSED_STAGING_FILES},

        #Filesystem_serving
        {'name':'FILESYSTEM_FILESERVING_ENABLE', 'value':filesystem_serving_settings.FILESERVING_ENABLE},
        {'name':'FILESYSTEM_FILESERVING_PATH', 'value':filesystem_serving_settings.FILESERVING_PATH, 'exists':True},
        {'name':'FILESYSTEM_SLUGIFY_PATHS', 'value':filesystem_serving_settings.SLUGIFY_PATHS},
        {'name':'FILESYSTEM_MAX_RENAME_COUNT', 'value':filesystem_serving_settings.MAX_RENAME_COUNT},
        
        
        #Common
        {'name':'COMMON_TEMPORARY_DIRECTORY', 'value':common_settings.TEMPORARY_DIRECTORY, 'exists':True},

        #Converter
        {'name':'CONVERTER_CONVERT_PATH', 'value':converter_settings.CONVERT_PATH, 'exists':True},
        {'name':'CONVERTER_UNPAPER_PATH', 'value':converter_settings.UNPAPER_PATH, 'exists':True},
        {'name':'CONVERTER_IDENTIFY_PATH', 'value':converter_settings.IDENTIFY_PATH, 'exists':True},
        {'name':'CONVERTER_OCR_OPTIONS', 'value':converter_settings.OCR_OPTIONS},
        {'name':'CONVERTER_DEFAULT_OPTIONS', 'value':converter_settings.DEFAULT_OPTIONS},
        {'name':'CONVERTER_LOW_QUALITY_OPTIONS', 'value':converter_settings.LOW_QUALITY_OPTIONS},
        {'name':'CONVERTER_HIGH_QUALITY_OPTIONS', 'value':converter_settings.HIGH_QUALITY_OPTIONS},

        #ocr
        {'name':'OCR_TESSERACT_PATH', 'value':ocr_settings.TESSERACT_PATH, 'exists':True},
        {'name':'OCR_TESSERACT_LANGUAGE', 'value':ocr_settings.TESSERACT_LANGUAGE},
        {'name':'OCR_MAX_CONCURRENT_EXECUTION', 'value':ocr_settings.MAX_CONCURRENT_EXECUTION},
    ]
    
    context={
        'title':_(u'settings'),
        'object_list':settings,
        'hide_link':True,
        'hide_object':True,
        'extra_columns':[
            {'name':_(u'name'), 'attribute':'name'},
            {'name':_(u'value'), 'attribute': lambda x: _return_type(x['value'])},
            {'name':_(u'exists'), 'attribute':lambda x: _exists(x['value']) if 'exists' in x else ''},
        ]
    }
    
    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))
        

def _return_type(value):
    if isinstance(value, types.FunctionType):
        return _(u'function found')
    elif isinstance(value, types.ClassType):
        return _(u'class found')
    elif isinstance(value, types.TypeType):
        return _(u'class found')
    elif isinstance(value, types.DictType) or isinstance(value, types.DictionaryType):
        return ','.join(list(value))
    else:
        return value

def _exists(path):
    try:
        return os.path.exists(path)
    except Exception, exc:
        return exc


def blank_menu(request):
    return render_to_response('generic_template.html', {
        'title':_(u'Tools menu'),
        'paragraphs':[
            _(u'"Find all duplicates": Search all the documents\' checksums and return a list of the exact matches.'),
            _(u'"Recreate index links": Deletes and creates from scratch all the file system indexing links.')
        ],
        },
    context_instance=RequestContext(request))    
