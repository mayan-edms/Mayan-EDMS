from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.html_widgets import TwoStateWidget
from mayan.apps.common.menus import (
    menu_list_facet, menu_multi_item, menu_object, menu_secondary, menu_setup,
    menu_tools
)
from mayan.apps.events.classes import ModelEventType
from mayan.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list
)
from mayan.apps.navigation.classes import SourceColumn

from .classes import MailerBackend
from .events import event_email_sent
from .links import (
    link_send_document_link, link_send_document, link_send_multiple_document,
    link_send_multiple_document_link, link_system_mailer_error_log,
    link_user_mailer_create, link_user_mailer_delete, link_user_mailer_edit,
    link_user_mailer_list, link_user_mailer_log_list, link_user_mailer_setup,
    link_user_mailer_test
)
from .permissions import (
    permission_mailing_link, permission_mailing_send_document,
    permission_user_mailer_delete, permission_user_mailer_edit,
    permission_user_mailer_use, permission_user_mailer_view,
)


class MailerApp(MayanAppConfig):
    app_namespace = 'mailer'
    app_url = 'mailer'
    has_tests = True
    name = 'mayan.apps.mailer'
    verbose_name = _('Mailer')

    def ready(self):
        super(MailerApp, self).ready()
        from actstream import registry

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        LogEntry = self.get_model(model_name='LogEntry')
        UserMailer = self.get_model(model_name='UserMailer')
        UserMailerLogEntry = self.get_model(model_name='UserMailerLogEntry')

        MailerBackend.initialize()

        ModelEventType.register(
            model=UserMailer, event_types=(event_email_sent,)
        )

        SourceColumn(
            source=LogEntry, label=_('Date and time'), attribute='datetime'
        )
        SourceColumn(
            source=LogEntry, label=_('Message'), attribute='message'
        )
        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=UserMailer
        )
        SourceColumn(
            attribute='default', include_label=True, is_sortable=True,
            source=UserMailer, widget=TwoStateWidget
        )
        SourceColumn(
            attribute='enabled', include_label=True, is_sortable=True,
            source=UserMailer, widget=TwoStateWidget
        )
        SourceColumn(
            attribute='backend_label', include_label=True, source=UserMailer
        )
        SourceColumn(
            attribute='datetime', label=_('Date and time'),
            source=UserMailerLogEntry
        )
        SourceColumn(
            attribute='message', label=_('Message'), source=UserMailerLogEntry
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_mailing_link, permission_mailing_send_document
            )
        )

        ModelPermission.register(
            model=UserMailer, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_user_mailer_delete, permission_user_mailer_edit,
                permission_user_mailer_view, permission_user_mailer_use
            )
        )

        menu_list_facet.bind_links(
            links=(
                link_acl_list, link_events_for_object,
                link_object_event_types_user_subcriptions_list,
                link_user_mailer_log_list
            ), sources=(UserMailer,)
        )

        menu_multi_item.bind_links(
            links=(
                link_send_multiple_document, link_send_multiple_document_link
            ), sources=(Document,)
        )

        menu_object.bind_links(
            links=(
                link_send_document_link, link_send_document
            ), sources=(Document,)
        )

        menu_object.bind_links(
            links=(
                link_user_mailer_delete, link_user_mailer_edit,
                link_user_mailer_test
            ), sources=(UserMailer,)
        )

        menu_secondary.bind_links(
            links=(
                link_user_mailer_list, link_user_mailer_create,
            ), sources=(
                UserMailer, 'mailer:user_mailer_list',
                'mailer:user_mailer_create'
            )
        )

        menu_tools.bind_links(links=(link_system_mailer_error_log,))

        menu_setup.bind_links(links=(link_user_mailer_setup,))

        registry.register(UserMailer)
