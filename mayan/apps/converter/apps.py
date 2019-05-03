from __future__ import unicode_literals

from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_object, menu_secondary
from mayan.apps.navigation.classes import SourceColumn

from .dependencies import *  # NOQA
from .links import (
    link_transformation_create, link_transformation_delete,
    link_transformation_edit
)


class ConverterApp(MayanAppConfig):
    app_namespace = 'converter'
    app_url = 'converter'
    has_tests = True
    name = 'mayan.apps.converter'
    verbose_name = _('Converter')

    def ready(self):
        super(ConverterApp, self).ready()

        Transformation = self.get_model(model_name='Transformation')

        SourceColumn(attribute='order', source=Transformation)
        SourceColumn(
            source=Transformation, label=_('Transformation'),
            func=lambda context: force_text(context['object'])
        )
        SourceColumn(
            attribute='arguments', source=Transformation
        )

        menu_object.bind_links(
            links=(link_transformation_edit, link_transformation_delete),
            sources=(Transformation,)
        )
        menu_secondary.bind_links(
            links=(link_transformation_create,), sources=(Transformation,)
        )
        menu_secondary.bind_links(
            links=(link_transformation_create,),
            sources=(
                'converter:transformation_create',
                'converter:transformation_list'
            )
        )
