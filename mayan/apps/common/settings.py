from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_COMMON_COLLAPSE_LIST_MENU_LIST_FACET,
    DEFAULT_COMMON_COLLAPSE_LIST_MENU_OBJECT,
    DEFAULT_COMMON_DB_SYNC_TASK_DELAY, DEFAULT_COMMON_DISABLED_APPS,
    DEFAULT_COMMON_EXTRA_APPS, DEFAULT_COMMON_HOME_VIEW,
    DEFAULT_COMMON_PROJECT_TITLE, DEFAULT_COMMON_PROJECT_URL
)

namespace = SettingNamespace(
    label=_('Common'), name='common', version='0002'
)

setting_collapse_list_menu_list_facet = namespace.add_setting(
    default=DEFAULT_COMMON_COLLAPSE_LIST_MENU_LIST_FACET,
    global_name='COMMON_COLLAPSE_LIST_MENU_LIST_FACET',
    help_text=_(
        'In list mode, show the "list facet" menu options as a dropdown '
        'menu instead of individual buttons.'
    )
)
setting_collapse_list_menu_object = namespace.add_setting(
    default=DEFAULT_COMMON_COLLAPSE_LIST_MENU_OBJECT,
    global_name='COMMON_COLLAPSE_LIST_MENU_OBJECT',
    help_text=_(
        'In list mode, show the "object" menu options as a dropdown menu '
        'instead of individual buttons.'
    )
)
settings_db_sync_task_delay = namespace.add_setting(
    default=DEFAULT_COMMON_DB_SYNC_TASK_DELAY,
    global_name='COMMON_DB_SYNC_TASK_DELAY', help_text=_(
        'Time to delay background tasks that depend on a database commit to '
        'propagate.'
    )
)
setting_disabled_apps = namespace.add_setting(
    default=DEFAULT_COMMON_DISABLED_APPS,
    global_name='COMMON_DISABLED_APPS', help_text=_(
        'A list of strings designating all applications that are to be '
        'removed from the list normally installed by Mayan EDMS. Each '
        'string should be a dotted Python path to: an application '
        'configuration class (preferred), or a package containing an '
        'application. Example: [\'app_1\', \'app_2\']'
    )
)
setting_extra_apps = namespace.add_setting(
    default=DEFAULT_COMMON_EXTRA_APPS, global_name='COMMON_EXTRA_APPS',
    help_text=_(
        'A list of strings designating all applications that are installed '
        'beyond those normally installed by Mayan EDMS. Each string '
        'should be a dotted Python path to: an application configuration '
        'class (preferred), or a package containing an application. '
        'Example: [\'app_1\', \'app_2\']'
    )
)
setting_home_view = namespace.add_setting(
    default=DEFAULT_COMMON_HOME_VIEW, global_name='COMMON_HOME_VIEW',
    help_text=_(
        'Name of the view attached to the brand anchor in the main menu. '
        'This is also the view to which users will be redirected after '
        'log in.'
    )
)
setting_project_title = namespace.add_setting(
    default=DEFAULT_COMMON_PROJECT_TITLE, global_name='COMMON_PROJECT_TITLE',
    help_text=_('Sets the project\'s name.')
)
setting_project_url = namespace.add_setting(
    default=DEFAULT_COMMON_PROJECT_URL, global_name='COMMON_PROJECT_URL',
    help_text=_('URL of the project\'s homepage.')
)
