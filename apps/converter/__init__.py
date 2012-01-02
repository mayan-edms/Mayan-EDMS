from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured

from navigation.api import register_sidebar_template
from project_tools.api import register_tool

from .utils import load_backend
from .conf.settings import GRAPHICS_BACKEND

formats_list = {'text': _('file formats'), 'view': 'formats_list', 'famfam': 'pictures', 'icon': 'pictures.png'}

register_sidebar_template(['formats_list'], 'converter_file_formats_help.html')

try:
    backend = load_backend().ConverterClass()
except ImproperlyConfigured:
    raise ImproperlyConfigured(u'Missing or incorrect converter backend: %s' % GRAPHICS_BACKEND)

register_tool(formats_list)
