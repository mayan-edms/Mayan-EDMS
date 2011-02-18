import os
import types

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from common.conf import settings as common_settings
from documents.conf import settings as documents_settings
from converter.conf import settings as converter_settings
from ocr.conf import settings as ocr_settings


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
        {'name':'DOCUMENTS_DELETE_LOCAL_ORIGINAL', 'value':documents_settings.DELETE_LOCAL_ORIGINAL},
        {'name':'DOCUMENTS_CHECKSUM_FUNCTION', 'value':documents_settings.CHECKSUM_FUNCTION},
        {'name':'DOCUMENTS_UUID_FUNTION', 'value':documents_settings.UUID_FUNCTION},
        {'name':'DOCUMENTS_STORAGE_BACKEND', 'value':documents_settings.STORAGE_BACKEND},
        {'name':'DOCUMENTS_STORAGE_DIRECTORY_NAME', 'value':documents_settings.STORAGE_DIRECTORY_NAME},
        {'name':'DOCUMENTS_PREVIEW_SIZE', 'value':documents_settings.PREVIEW_SIZE},
        {'name':'DOCUMENTS_THUMBNAIL_SIZE', 'value':documents_settings.THUMBNAIL_SIZE},
        {'name':'DOCUMENTS_DISPLAY_SIZE', 'value':documents_settings.DISPLAY_SIZE},
        {'name':'DOCUMENTS_FILESYSTEM_FILESERVING_ENABLE', 'value':documents_settings.FILESYSTEM_FILESERVING_ENABLE},
        {'name':'DOCUMENTS_FILESYSTEM_FILESERVING_PATH', 'value':documents_settings.FILESYSTEM_FILESERVING_PATH, 'exists':True},
        {'name':'DOCUMENTS_SLUGIFY_PATHS', 'value':documents_settings.FILESYSTEM_SLUGIFY_PATHS},
        {'name':'DOCUMENTS_FILESYSTEM_MAX_RENAME_COUNT', 'value':documents_settings.FILESYSTEM_MAX_RENAME_COUNT},
        {'name':'DOCUMENTS_AUTOMATIC_OCR', 'value':documents_settings.AUTOMATIC_OCR},
        
        #Common
        {'name':'COMMON_TEMPORARY_DIRECTORY', 'value':common_settings.TEMPORARY_DIRECTORY, 'exists':True},

        #Converter
        {'name':'CONVERTER_CONVERT_PATH', 'value':converter_settings.CONVERT_PATH, 'exists':True},
        {'name':'CONVERTER_OCR_OPTIONS', 'value':converter_settings.OCR_OPTIONS},

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
            {'name':_(u'value'), 'attribute': lambda x: return_type(x['value'])},
            {'name':_(u'exists'), 'attribute':lambda x: exists(x['value']) if 'exists' in x else ''},
        ]
    }
    
    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))
        

def return_type(value):
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

def exists(path):
    try:
        return os.path.exists(path)
    except Exception, exc:
        return exc
