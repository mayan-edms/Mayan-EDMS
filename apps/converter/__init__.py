from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured

from navigation.api import register_sidebar_template, Link
from project_tools.api import register_tool

from .utils import load_backend
from .conf.settings import GRAPHICS_BACKEND

def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser

formats_list = Link(text=_('file formats'), view='formats_list', sprite='pictures', icon='pictures.png', condition=is_superuser, children_view_regex=[r'formats_list'])

register_sidebar_template(['formats_list'], 'converter_file_formats_help.html')

try:
    backend = load_backend().ConverterClass()
except ImproperlyConfigured:
    raise ImproperlyConfigured(u'Missing or incorrect converter backend: %s' % GRAPHICS_BACKEND)

register_tool(formats_list)
