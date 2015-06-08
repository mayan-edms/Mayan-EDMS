from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from common import menu_object, menu_sidebar

from .links import (
    link_transformation_create, link_transformation_delete,
    link_transformation_edit
)
from .models import Transformation


class ConverterApp(apps.AppConfig):
    name = 'converter'
    verbose_name = _('Converter')

    def ready(self):
        menu_sidebar.bind_links(links=[link_transformation_create], sources=[Transformation])
        menu_sidebar.bind_links(links=[link_transformation_create], sources=['converter:transformation_create', 'converter:transformation_list'])
        menu_object.bind_links(links=[link_transformation_edit, link_transformation_delete], sources=[Transformation])
