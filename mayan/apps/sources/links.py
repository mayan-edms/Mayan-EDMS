import logging

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.permissions import (
    permission_document_create, permission_document_file_new
)
from mayan.apps.navigation.classes import Link

from .icons import (
    icon_document_create_multiple, icon_document_file_upload,
    icon_source_backend_selection, icon_source_test,
    icon_source_delete, icon_source_edit, icon_source_list,
)
from .permissions import (
    permission_sources_create, permission_sources_delete,
    permission_sources_edit, permission_sources_view
)

logger = logging.getLogger(name=__name__)


def factory_conditional_active_by_source(source):
    def conditional_active_by_source(context, resolved_link):
        return context.get('source', None) == source

    return conditional_active_by_source


def condition_document_creation_access(context, resolved_object):
    AccessControlList = apps.get_model(
        app_label='acls', model_name='AccessControlList'
    )
    DocumentType = apps.get_model(
        app_label='documents', model_name='DocumentType'
    )
    Source = apps.get_model(
        app_label='sources', model_name='Source'
    )

    document_type_access = AccessControlList.objects.restrict_queryset(
        permission=permission_document_create,
        queryset=DocumentType.objects.all(), user=context.request.user
    ).exists()

    source_access = AccessControlList.objects.restrict_queryset(
        permission=permission_document_create,
        queryset=Source.objects.all(), user=context.request.user
    ).exists()

    return document_type_access and source_access


def condition_document_new_files_allowed(context, resolved_object):
    if resolved_object:
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentFile = apps.get_model(
            app_label='documents', model_name='DocumentFile'
        )
        Source = apps.get_model(
            app_label='sources', model_name='Source'
        )

        new_document_files_allowed = False

        try:
            DocumentFile.execute_pre_create_hooks(
                kwargs={
                    'document': context['object'],
                    'file_object': None,
                    'user': context.request.user
                }
            )
        except Exception as exception:
            logger.warning(
                'execute_pre_create_hooks raised and exception: %s', exception
            )
        else:
            new_document_files_allowed = True

        document_access = AccessControlList.objects.restrict_queryset(
            permission=permission_document_file_new,
            queryset=Document.valid.filter(pk__in=(resolved_object.pk,)),
            user=context.request.user
        ).exists()

        source_access = AccessControlList.objects.restrict_queryset(
            permission=permission_document_file_new,
            queryset=Source.objects.all(), user=context.request.user
        ).exists()

        return new_document_files_allowed and document_access and source_access


def condition_source_is_not_interactive(context, resolved_object):
    source = context.get('resolved_object', None)
    if source:
        return not getattr(source.get_backend(), 'is_interactive', False)


link_document_create_multiple = Link(
    condition=condition_document_creation_access,
    icon=icon_document_create_multiple, text=_('New document'),
    view='sources:document_create_multiple'
)
link_document_file_upload = Link(
    condition=condition_document_new_files_allowed,
    kwargs={'document_id': 'resolved_object.pk'},
    icon=icon_document_file_upload,
    text=_('Upload new file'), view='sources:document_file_upload',
)

link_source_backend_selection = Link(
    icon=icon_source_backend_selection,
    permissions=(permission_sources_create,),
    text=_('Create source'),
    view='sources:source_backend_selection'
)
link_source_delete = Link(
    args=('resolved_object.pk',), icon=icon_source_delete,
    permissions=(permission_sources_delete,), tags='dangerous',
    text=_('Delete'), view='sources:source_delete',
)
link_source_edit = Link(
    args=('resolved_object.pk',), icon=icon_source_edit,
    permissions=(permission_sources_edit,), text=_('Edit'),
    view='sources:source_edit',
)
link_source_list = Link(
    icon=icon_source_list,
    permissions=(permission_sources_view,), text=_('Sources'),
    view='sources:source_list'
)
link_source_test = Link(
    args=('resolved_object.pk',),
    condition=condition_source_is_not_interactive,
    icon=icon_source_test,
    permissions=(permission_sources_view,), text=_('Test'),
    view='sources:source_test',
)
