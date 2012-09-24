from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_index_setup
from .links import index_setup, link_menu

label = _(u'Document indexing')
description = _(u'Handles organization indexing for documents.')
dependencies = ['app_registry', 'icons', 'navigation', 'metadata']
icon = icon_index_setup
setup_links = [index_setup]
menu_links = [link_menu]
bootstrap_models = ['index', 'indextemplatenode']

"""

from django.utils.translation import ugettext_lazy as _

from common.utils import proper_name
from smart_settings.api import Setting, SettingNamespace

available_indexing_functions = {
    'proper_name': proper_name
}

namespace = SettingNamespace('document_indexing', _(u'Indexing'), module='document_indexing.conf.settings', sprite='tab')

# Definition

Setting(
    namespace=namespace,
    name='AVAILABLE_INDEXING_FUNCTIONS',
    global_name='DOCUMENT_INDEXING_AVAILABLE_INDEXING_FUNCTIONS',
    default=available_indexing_functions,
)

Setting(
    namespace=namespace,
    name='SUFFIX_SEPARATOR',
    global_name='DOCUMENT_INDEXING_SUFFIX_SEPARATOR',
    default=u'_',
)

# Filesystem serving

Setting(
    namespace=namespace,
    name='SLUGIFY_PATHS',
    global_name='DOCUMENT_INDEXING_FILESYSTEM_SLUGIFY_PATHS',
    default=False,
)

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
