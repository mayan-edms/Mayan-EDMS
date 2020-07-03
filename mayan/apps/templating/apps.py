from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_facet

from .classes import Template
from .links import link_document_template_sandbox
from .permissions import permission_template_sandbox


class TemplatingApp(MayanAppConfig):
    app_namespace = 'templating'
    app_url = 'templating'
    has_static_media = True
    has_tests = True
    name = 'mayan.apps.templating'
    verbose_name = _('Templating')

    def ready(self):
        super(TemplatingApp, self).ready()
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_template_sandbox,
            )
        )

        menu_facet.bind_links(
            links=(
                link_document_template_sandbox,
            ), sources=(Document,)
        )
