from __future__ import unicode_literals

from django.template import Library
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

register = Library()

from ..classes import SearchModel


@register.simple_tag
def get_search_models():
    return SearchModel.all()
