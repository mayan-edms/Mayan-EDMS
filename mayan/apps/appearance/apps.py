from django.conf import settings
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import (
    permission_acl_edit, permission_acl_view
)
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import ModelCopy
from mayan.apps.common.menus import (
    menu_list_facet, menu_object, menu_secondary, menu_setup, menu_user
)
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.navigation.classes import SourceColumn

from .events import event_theme_edited
from .links import (
    link_current_user_theme_settings_edit, link_theme_create,
    link_theme_delete, link_theme_edit, link_theme_list, link_theme_setup
)
from .handlers import handler_user_theme_setting_create
from .permissions import (
    permission_theme_delete, permission_theme_edit, permission_theme_view
)


class AppearanceApp(MayanAppConfig):
    app_namespace = 'appearance'
    app_url = 'appearance'
    has_static_media = True
    has_tests = True
    name = 'mayan.apps.appearance'
    static_media_ignore_patterns = (
        'AUTHORS*', 'CHANGE*', 'CONTRIBUT*', 'CODE_OF_CONDUCT*', 'Grunt*',
        'LICENSE*', 'MAINTAIN*', 'README*', '*.less', '*.md', '*.nupkg',
        '*.nuspec', '*.scss*', '*.sh', '*tests*', 'bower*', 'composer.json*',
        'demo*', 'grunt*', 'gulp*', 'install', 'less', 'package.json*',
        'package-lock*', 'test', 'tests', 'variable*',
        'appearance/node_modules/@fancyapps/fancybox/docs/*',
        'appearance/node_modules/@fancyapps/fancybox/src/*',
        'appearance/node_modules/@fortawesome/fontawesome-free/svgs/*',
        'appearance/node_modules/bootswatch/docs/*',
        'appearance/node_modules/jquery/src/*',
        'appearance/node_modules/jquery-form/_config.yml',
        'appearance/node_modules/jquery-form/form.jquery.json',
        'appearance/node_modules/jquery-form/docs/*',
        'appearance/node_modules/jquery-form/src/*',
        'appearance/node_modules/select2/src/*',
        'appearance/node_modules/toastr/karma.conf.js',
        'appearance/node_modules/toastr/toastr.js',
        'appearance/node_modules/toastr/toastr-icon.png',
        'appearance/node_modules/toastr/nuget/*',
    )
    verbose_name = _('Appearance')

    def ready(self):
        super().ready()

        Theme = self.get_model(model_name='Theme')

        ModelCopy(
            model=Theme, bind_link=True, register_permission=True
        ).add_fields(
            field_names=('label', 'stylesheet',),
        )

        EventModelRegistry.register(model=Theme)

        ModelEventType.register(
            event_types=(
                event_theme_edited,
            ), model=Theme
        )

        ModelPermission.register(
            model=Theme, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_theme_delete, permission_theme_edit,
                permission_theme_view
            )
        )

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=Theme
        )

        post_save.connect(
            dispatch_uid='appearance_handler_user_theme_setting_create',
            receiver=handler_user_theme_setting_create,
            sender=settings.AUTH_USER_MODEL
        )

        menu_list_facet.bind_links(
            links=(link_acl_list,), sources=(Theme,)
        )
        menu_object.bind_links(
            links=(
                link_theme_delete, link_theme_edit
            ), sources=(Theme,)
        )

        menu_secondary.bind_links(
            links=(link_theme_list, link_theme_create),
            sources=(
                Theme, 'appearance:theme_list', 'appearance:theme_create'
            )
        )
        menu_setup.bind_links(links=(link_theme_setup,))

        menu_user.bind_links(
            links=(
                link_current_user_theme_settings_edit,
            ), position=60
        )
