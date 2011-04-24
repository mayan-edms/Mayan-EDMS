import types

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from common.utils import exists_with_famfam

from common.conf import settings as common_settings
from documents.conf import settings as documents_settings
from documents.statistics import get_statistics as documents_statistics
from converter.conf import settings as converter_settings
from ocr.conf import settings as ocr_settings
from ocr.statistics import get_statistics as ocr_statistics
from filesystem_serving.conf import settings as filesystem_serving_settings
from dynamic_search.conf import settings as search_settings
from main.conf import settings as main_settings

from main.api import diagnostics


def home(request):
    return render_to_response('home.html', {},
    context_instance=RequestContext(request))


def check_settings(request):
    settings = [
        {'name': 'MAIN_SIDE_BAR_SEARCH',
            'value': main_settings.SIDE_BAR_SEARCH,
            'description': main_settings.setting_description},

        {'name': 'DOCUMENTS_METADATA_AVAILABLE_FUNCTIONS', 'value': documents_settings.AVAILABLE_FUNCTIONS},
        {'name': 'DOCUMENTS_METADATA_AVAILABLE_MODELS', 'value': documents_settings.AVAILABLE_MODELS},
        {'name': 'DOCUMENTS_INDEXING_AVAILABLE_INDEXING_FUNCTIONS', 'value': documents_settings.AVAILABLE_INDEXING_FUNCTIONS},
        {'name': 'DOCUMENTS_USE_STAGING_DIRECTORY', 'value': documents_settings.USE_STAGING_DIRECTORY},
        {'name': 'DOCUMENTS_STAGING_DIRECTORY', 'value': documents_settings.STAGING_DIRECTORY, 'exists': True},
        {'name': 'DOCUMENTS_DELETE_STAGING_FILE_AFTER_UPLOAD', 'value': documents_settings.DELETE_STAGING_FILE_AFTER_UPLOAD},
        {'name': 'DOCUMENTS_STAGING_FILES_PREVIEW_SIZE', 'value': documents_settings.STAGING_FILES_PREVIEW_SIZE},
        {'name': 'DOCUMENTS_CHECKSUM_FUNCTION', 'value': documents_settings.CHECKSUM_FUNCTION},
        {'name': 'DOCUMENTS_UUID_FUNTION', 'value': documents_settings.UUID_FUNCTION},
        {'name': 'DOCUMENTS_STORAGE_BACKEND', 'value': documents_settings.STORAGE_BACKEND},
        {'name': 'DOCUMENTS_PREVIEW_SIZE', 'value': documents_settings.PREVIEW_SIZE},
        {'name': 'DOCUMENTS_THUMBNAIL_SIZE', 'value': documents_settings.THUMBNAIL_SIZE},
        {'name': 'DOCUMENTS_DISPLAY_SIZE', 'value': documents_settings.DISPLAY_SIZE},
        {'name': 'DOCUMENTS_ENABLE_SINGLE_DOCUMENT_UPLOAD', 'value': documents_settings.ENABLE_SINGLE_DOCUMENT_UPLOAD},
        {'name': 'DOCUMENTS_UNCOMPRESS_COMPRESSED_LOCAL_FILES', 'value': documents_settings.UNCOMPRESS_COMPRESSED_LOCAL_FILES},
        {'name': 'DOCUMENTS_UNCOMPRESS_COMPRESSED_STAGING_FILES', 'value': documents_settings.UNCOMPRESS_COMPRESSED_STAGING_FILES},
        {'name': 'DOCUMENTS_ZOOM_PERCENT_STEP', 'value': documents_settings.ZOOM_PERCENT_STEP},
        {'name': 'DOCUMENTS_ZOOM_MAX_LEVEL', 'value': documents_settings.ZOOM_MAX_LEVEL},
        {'name': 'DOCUMENTS_ZOOM_MIN_LEVEL', 'value': documents_settings.ZOOM_MIN_LEVEL},
        {'name': 'DOCUMENTS_ROTATION_STEP', 'value': documents_settings.ROTATION_STEP},

        #Groups
        {'name': 'DOCUMENTS_GROUP_SHOW_EMPTY', 'value': documents_settings.GROUP_SHOW_EMPTY},
        {'name': 'DOCUMENTS_RECENT_COUNT', 'value': documents_settings.RECENT_COUNT},

        #Filesystem_serving
        {'name': 'FILESYSTEM_FILESERVING_ENABLE', 'value': filesystem_serving_settings.FILESERVING_ENABLE},
        {'name': 'FILESYSTEM_FILESERVING_PATH', 'value': filesystem_serving_settings.FILESERVING_PATH, 'exists': True},
        {'name': 'FILESYSTEM_SLUGIFY_PATHS', 'value': filesystem_serving_settings.SLUGIFY_PATHS},
        {'name': 'FILESYSTEM_MAX_RENAME_COUNT', 'value': filesystem_serving_settings.MAX_RENAME_COUNT},

        # Common
        {'name': 'COMMON_TEMPORARY_DIRECTORY',
            'value': common_settings.TEMPORARY_DIRECTORY, 'exists': True,
            'description': common_settings.setting_description},

        # Converter
        {'name': 'CONVERTER_UNPAPER_PATH',
            'value': converter_settings.UNPAPER_PATH, 'exists': True,
            'description': converter_settings.setting_description},
        {'name': 'CONVERTER_IM_CONVERT_PATH',
            'value': converter_settings.IM_CONVERT_PATH, 'exists': True,
            'description': converter_settings.setting_description},
        {'name': 'CONVERTER_IM_IDENTIFY_PATH',
            'value': converter_settings.IM_IDENTIFY_PATH, 'exists': True,
            'description': converter_settings.setting_description},
        {'name': 'CONVERTER_GM_PATH',
            'value': converter_settings.GM_PATH, 'exists': True,
            'description': converter_settings.setting_description},
        {'name': 'CONVERTER_GM_SETTINGS', 'value': converter_settings.GM_SETTINGS},
        {'name': 'CONVERTER_GRAPHICS_BACKEND',
            'value': converter_settings.GRAPHICS_BACKEND,
            'description': converter_settings.setting_description},
        {'name': 'CONVERTER_UNOCONV_PATH',
            'value': converter_settings.UNOCONV_PATH, 'exists': True},
        {'name': 'CONVERTER_OCR_OPTIONS', 'value': converter_settings.OCR_OPTIONS},
        {'name': 'CONVERTER_DEFAULT_OPTIONS', 'value': converter_settings.DEFAULT_OPTIONS},
        {'name': 'CONVERTER_LOW_QUALITY_OPTIONS', 'value': converter_settings.LOW_QUALITY_OPTIONS},
        {'name': 'CONVERTER_HIGH_QUALITY_OPTIONS', 'value': converter_settings.HIGH_QUALITY_OPTIONS},

        # OCR
        {'name': 'OCR_AUTOMATIC_OCR', 'value': ocr_settings.AUTOMATIC_OCR},
        {'name': 'OCR_TESSERACT_PATH', 'value': ocr_settings.TESSERACT_PATH, 'exists': True},
        {'name': 'OCR_TESSERACT_LANGUAGE', 'value': ocr_settings.TESSERACT_LANGUAGE},
        {'name': 'OCR_NODE_CONCURRENT_EXECUTION', 'value': ocr_settings.NODE_CONCURRENT_EXECUTION},
        {'name': 'OCR_REPLICATION_DELAY', 'value': ocr_settings.REPLICATION_DELAY},
        {'name': 'OCR_PDFTOTEXT_PATH', 'value': ocr_settings.PDFTOTEXT_PATH, 'exists': True},
        {'name': 'OCR_QUEUE_PROCESSING_INTERVAL', 'value': ocr_settings.QUEUE_PROCESSING_INTERVAL},

        # Search
        {'name': 'SEARCH_LIMIT', 'value': search_settings.LIMIT},
    ]

    context = {
        'title': _(u'settings'),
        'object_list': settings,
        'hide_link': True,
        'hide_object': True,
        'extra_columns': [
            {'name': _(u'name'), 'attribute': 'name'},
            {'name': _(u'value'), 'attribute': lambda x: _return_type(x['value'])},
            {'name': _(u'description'), 'attribute': lambda x: x.get('description', {}).get(x['name'], '')},
            {'name': _(u'exists'), 'attribute': lambda x: exists_with_famfam(x['value']) if 'exists' in x else ''},
        ]
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def _return_type(value):
    if isinstance(value, types.FunctionType):
        return value.__doc__ if value.__doc__ else _(u'function found')
    elif isinstance(value, types.ClassType):
        return _(u'class found: %s') % unicode(value).split("'")[1].split('.')[-1]
    elif isinstance(value, types.TypeType):
        return _(u'class found: %s') % unicode(value).split("'")[1].split('.')[-1]
    elif isinstance(value, types.DictType) or isinstance(value, types.DictionaryType):
        return ','.join(list(value))
    else:
        return value


def blank_menu(request):
    return render_to_response('generic_template.html', {
        'title': _(u'Tools menu'),
        'paragraphs': [
            _(u'"Find all duplicates": Search all the documents\' checksums and return a list of the exact matches.'),
            _(u'"Recreate index links": Deletes and creates from scratch all the file system indexing links.'),
            _(u'"Clean up pages content": Runs a language filter to remove common OCR mistakes from document pages content.')
        ],
    },
    context_instance=RequestContext(request))


def statistics(request):
    blocks = []
    blocks.append(documents_statistics())
    blocks.append(ocr_statistics())

    return render_to_response('statistics.html', {
        'blocks': blocks,
        'title': _(u'Statistics')
    },
    context_instance=RequestContext(request))


def diagnostics_view(request):
    return render_to_response('diagnostics.html', {
        'blocks': diagnostics,
        'title': _(u'Diagnostics')
    },
    context_instance=RequestContext(request))
