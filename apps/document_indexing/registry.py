from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from common.utils import proper_name
from smart_settings import 

from .icons import icon_index_setup
from .links import index_setup, link_menu
from .literals import DEFAULT_SUFFIX_SEPARATOR, DEFAULT_MAX_SUFFIX_COUNT

available_indexing_functions = {
    'proper_name': proper_name
}

label = _(u'Document indexing')
description = _(u'Handles organization indexing for documents.')
dependencies = ['app_registry', 'icons', 'navigation', 'metadata']
icon = icon_index_setup
setup_links = [index_setup]
menu_links = [link_menu]
bootstrap_models = ['index', 'indextemplatenode']

settings = [
    {
        'name': 'AVAILABLE_INDEXING_FUNCTIONS',
        'default': available_indexing_functions,
        'scopes': [LocalScope()],
    },
    {
        'name': 'SUFFIX_SEPARATOR',
        'default': DEFAULT_SUFFIX_SEPARATOR,
        'scopes': [LocalScope()],
    },    
    {
        'name': 'SLUGIFY_PATHS',
        'default': False,
        'scopes': [LocalScope()],
    },    
    {
        'name': 'MAX_SUFFIX_COUNT',
        'default': DEFAULT_MAX_SUFFIX_COUNT,
        'scopes': [LocalScope()],
    }, 
    {
        'name': 'FILESYSTEM_SERVING',
        'default': {},
        'description': _(u'A dictionary that maps the index name and where on the filesystem that index will be mirrored.'),
        'scopes': [LocalScope()],
    }, 
]
"""

# Definition



# Filesystem serving


Setting(
    namespace=namespace,
    name='MAX_SUFFIX_COUNT',
    global_name='DOCUMENT_INDEXING_FILESYSTEM_MAX_SUFFIX_COUNT',
    default=1000,
)

Setting(
    namespace=namespace,
    name='FILESYSTEM_SERVING',
    global_name='DOCUMENT_INDEXING_FILESYSTEM_SERVING',
    default={},
    description=_(u'A dictionary that maps the index name and where on the filesystem that index will be mirrored.'),
)
"""
