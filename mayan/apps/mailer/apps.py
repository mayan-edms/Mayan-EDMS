from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.permissions import (
    permission_acl_edit, permission_acl_view
)
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import ModelCopy
from mayan.apps.common.menus import (
    menu_multi_item, menu_object, menu_secondary, menu_setup
)
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.logging.classes import ErrorLog
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.views.html_widgets import TwoStateWidget

from .classes import MailerBackend
from .events import event_email_sent
from .links import (
    link_send_document_link_single, link_send_document_link_multiple,
    link_send_document_file_attachment_single,
    link_send_document_file_attachment_multiple,
    link_send_document_file_link_single,
    link_send_document_file_link_multiple,
    link_send_document_version_attachment_single,
    link_send_document_version_attachment_multiple,
    link_send_document_version_link_single,
    link_send_document_version_link_multiple,
    link_user_mailer_create, link_user_mailer_delete, link_user_mailer_edit,
    link_user_mailer_list, link_user_mailer_setup, link_user_mailer_test
)
from .permissions import (
    permission_send_document_link, permission_send_document_file_attachment,
    permission_send_document_file_link,
    permission_send_document_version_attachment,
    permission_send_document_version_link, permission_user_mailer_delete,
    permission_user_mailer_edit, permission_user_mailer_use,
    permission_user_mailer_view
)


class MailerApp(MayanAppConfig):
    app_namespace = 'mailer'
    app_url = 'mailer'
    has_tests = True
    name = 'mayan.apps.mailer'
    verbose_name = _('Mailer')

    def ready(self):
        super().ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentFile = apps.get_model(
            app_label='documents', model_name='DocumentFile'
        )
        DocumentVersion = apps.get_model(
            app_label='documents', model_name='DocumentVersion'
        )

        UserMailer = self.get_model(model_name='UserMailer')

        error_log = ErrorLog(app_config=self)
        error_log.register_model(model=UserMailer, register_permission=True)

        EventModelRegistry.register(model=UserMailer)

        MailerBackend.load_modules()

        ModelCopy(
            model=UserMailer, bind_link=True, register_permission=True
        ).add_fields(
            field_names=(
                'label', 'enabled', 'backend_path', 'backend_data'
            ), field_values={
                'default': False
            }
        )

        ModelEventType.register(
            model=UserMailer, event_types=(event_email_sent,)
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
            attribute='get_backend_label', include_label=True,
            source=UserMailer
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_send_document_link,
            )
        )
        ModelPermission.register(
            model=DocumentFile, permissions=(
                permission_send_document_file_attachment,
                permission_send_document_file_link
            )
        )
        ModelPermission.register(
            model=DocumentVersion, permissions=(
                permission_send_document_version_attachment,
                permission_send_document_version_link
            )
        )

        ModelPermission.register(
            model=UserMailer, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_user_mailer_delete, permission_user_mailer_edit,
                permission_user_mailer_view, permission_user_mailer_use
            )
        )

        # Document

        menu_multi_item.bind_links(
            links=(
                link_send_document_link_multiple,
            ), sources=(Document,)
        )

        menu_object.bind_links(
            links=(
                link_send_document_link_single,
            ), sources=(Document,)
        )

        # Document file

        menu_multi_item.bind_links(
            links=(
                link_send_document_file_attachment_multiple,
                link_send_document_file_link_multiple
            ), sources=(DocumentFile,)
        )

        menu_object.bind_links(
            links=(
                link_send_document_file_link_single,
                link_send_document_file_attachment_single
            ), sources=(DocumentFile,)
        )

        # Document version

        menu_multi_item.bind_links(
            links=(
                link_send_document_version_attachment_multiple,
                link_send_document_version_link_multiple
            ), sources=(DocumentVersion,)
        )

        menu_object.bind_links(
            links=(
                link_send_document_version_link_single,
                link_send_document_version_attachment_single
            ), sources=(DocumentVersion,)
        )

        # Mailing profile

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

        menu_setup.bind_links(links=(link_user_mailer_setup,))
