from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_object, menu_secondary
from mayan.apps.navigation.classes import SourceColumn

from .links import (
    link_transformation_delete, link_transformation_edit,
    link_transformation_select
)


class ConverterApp(MayanAppConfig):
    app_namespace = 'converter'
    app_url = 'converter'
    has_tests = True
    name = 'mayan.apps.converter'
    verbose_name = _('Converter')

    def ready(self):
        super(ConverterApp, self).ready()

        LayerTransformation = self.get_model(model_name='LayerTransformation')

        ModelPermission.register_inheritance(
            model=LayerTransformation,
            related='object_layer__content_object',
        )

        SourceColumn(
            attribute='order', is_identifier=True, source=LayerTransformation
        )
        SourceColumn(
            func=lambda context: force_text(context['object']),
            include_label=True, label=_('Transformation'),
            source=LayerTransformation
        )
        SourceColumn(
            attribute='arguments', include_label=True,
            source=LayerTransformation
        )

        menu_object.bind_links(
            links=(link_transformation_edit, link_transformation_delete),
            sources=(LayerTransformation,)
        )
        menu_secondary.bind_links(
            links=(link_transformation_select,), sources=(LayerTransformation,)
        )
        menu_secondary.bind_links(
            links=(link_transformation_select,),
            sources=(
                'converter:transformation_create',
                'converter:transformation_list'
            )
        )
