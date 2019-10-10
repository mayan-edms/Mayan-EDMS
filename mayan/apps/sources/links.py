from __future__ import absolute_import, unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.permissions import (
    permission_document_create, permission_document_new_version
)
from mayan.apps.navigation.classes import Link

from .literals import (
    SOURCE_CHOICE_WEB_FORM, SOURCE_CHOICE_EMAIL_IMAP, SOURCE_CHOICE_EMAIL_POP3,
    SOURCE_CHOICE_SANE_SCANNER, SOURCE_CHOICE_STAGING, SOURCE_CHOICE_WATCH
)
from .permissions import (
    permission_sources_setup_create, permission_sources_setup_delete,
    permission_sources_setup_edit, permission_sources_setup_view
)


def condition_check_document_creation_acls(context):
    AccessControlList = apps.get_model(
        app_label='acls', model_name='AccessControlList'
    )
    DocumentType = apps.get_model(
        app_label='documents', model_name='DocumentType'
    )

    queryset = AccessControlList.objects.restrict_queryset(
        permission=permission_document_create,
        queryset=DocumentType.objects.all(), user=context['user']
    )

    if queryset:
        return True


def document_new_version_not_blocked(context):
    NewVersionBlock = apps.get_model(
        app_label='checkouts', model_name='NewVersionBlock'
    )

    return not NewVersionBlock.objects.is_blocked(context['object'])


link_document_create_multiple = Link(
    condition=condition_check_document_creation_acls,
    icon_class_path='mayan.apps.sources.icons.icon_document_create_multiple',
    text=_('New document'),
    view='sources:document_create_multiple'
)
link_setup_sources = Link(
    icon_class_path='mayan.apps.sources.icons.icon_setup_sources',
    permissions=(permission_sources_setup_view,), text=_('Sources'),
    view='sources:setup_source_list'
)
link_setup_source_create_imap_email = Link(
    args='"%s"' % SOURCE_CHOICE_EMAIL_IMAP,
    icon_class_path='mayan.apps.sources.icons.icon_source_create',
    permissions=(permission_sources_setup_create,),
    text=_('Add new IMAP email'), view='sources:setup_source_create',
)
link_setup_source_create_pop3_email = Link(
    args='"%s"' % SOURCE_CHOICE_EMAIL_POP3,
    icon_class_path='mayan.apps.sources.icons.icon_source_create',
    permissions=(permission_sources_setup_create,),
    text=_('Add new POP3 email'), view='sources:setup_source_create',
)
link_setup_source_create_staging_folder = Link(
    args='"%s"' % SOURCE_CHOICE_STAGING,
    icon_class_path='mayan.apps.sources.icons.icon_source_create',
    permissions=(permission_sources_setup_create,),
    text=_('Add new staging folder'), view='sources:setup_source_create',
)
link_setup_source_create_watch_folder = Link(
    args='"%s"' % SOURCE_CHOICE_WATCH,
    icon_class_path='mayan.apps.sources.icons.icon_source_create',
    permissions=(permission_sources_setup_create,),
    text=_('Add new watch folder'), view='sources:setup_source_create',
)
link_setup_source_create_webform = Link(
    args='"%s"' % SOURCE_CHOICE_WEB_FORM,
    icon_class_path='mayan.apps.sources.icons.icon_source_create',
    permissions=(permission_sources_setup_create,),
    text=_('Add new webform source'), view='sources:setup_source_create',
)
link_setup_source_create_sane_scanner = Link(
    args='"%s"' % SOURCE_CHOICE_SANE_SCANNER,
    icon_class_path='mayan.apps.sources.icons.icon_source_create',
    permissions=(permission_sources_setup_create,),
    text=_('Add new SANE scanner'), view='sources:setup_source_create',
)
link_setup_source_delete = Link(
    args=('resolved_object.pk',),
    icon_class_path='mayan.apps.sources.icons.icon_setup_source_delete',
    permissions=(permission_sources_setup_delete,), tags='dangerous',
    text=_('Delete'), view='sources:setup_source_delete',
)
link_setup_source_edit = Link(
    args=('resolved_object.pk',),
    icon_class_path='mayan.apps.sources.icons.icon_setup_source_edit',
    permissions=(permission_sources_setup_edit,), text=_('Edit'),
    view='sources:setup_source_edit',
)
link_source_list = Link(
    icon_class_path='mayan.apps.sources.icons.icon_source_list',
    permissions=(permission_sources_setup_view,), text=_('Document sources'),
    view='sources:setup_web_form_list'
)
link_staging_file_delete = Link(
    args=('source.pk', 'object.encoded_filename',), keep_query=True,
    icon_class_path='mayan.apps.sources.icons.icon_staging_file_delete',
    permissions=(permission_document_new_version, permission_document_create),
    tags='dangerous', text=_('Delete'), view='sources:staging_file_delete',
)
link_document_version_upload = Link(
    args='resolved_object.pk', condition=document_new_version_not_blocked,
    icon_class_path='mayan.apps.sources.icons.icon_document_version_upload',
    permissions=(permission_document_new_version,),
    text=_('Upload new version'), view='sources:document_version_upload',
)
link_setup_source_logs = Link(
    args=('resolved_object.pk',),
    permissions=(permission_sources_setup_view,), text=_('Logs'),
    view='sources:setup_source_logs',
)
link_setup_source_check_now = Link(
    args=('resolved_object.pk',),
    icon_class_path='mayan.apps.sources.icons.icon_setup_source_check_now',
    permissions=(permission_sources_setup_view,), text=_('Check now'),
    view='sources:setup_source_check',
)
