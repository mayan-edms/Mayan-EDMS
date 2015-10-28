from __future__ import absolute_import, unicode_literals

from datetime import timedelta

from kombu import Exchange, Queue

from django.utils.translation import ugettext_lazy as _

from actstream import registry

from acls import ModelPermission
from acls.links import link_acl_list
from acls.permissions import permission_acl_edit, permission_acl_view
from common import (
    MayanAppConfig, MissingItem, menu_facet, menu_front_page, menu_object,
    menu_secondary, menu_setup, menu_sidebar, menu_multi_item, menu_tools
)
from common.classes import ModelAttribute
from common.signals import post_initial_setup
from common.widgets import two_state_template
from converter.links import link_transformation_list
from converter.permissions import (
    permission_transformation_create,
    permission_transformation_delete, permission_transformation_edit,
    permission_transformation_view,
)
from events.links import link_events_for_object
from events.permissions import permission_events_view
from mayan.celery import app
from navigation import SourceColumn
from rest_api.classes import APIEndPoint
from statistics.classes import StatisticNamespace, CharJSLine

from .handlers import create_default_document_type
from .links import (
    link_clear_image_cache, link_document_clear_transformations,
    link_document_delete, link_document_document_type_edit,
    link_document_multiple_document_type_edit, link_document_download,
    link_document_edit, link_document_list, link_document_list_deleted,
    link_document_list_recent, link_document_multiple_delete,
    link_document_multiple_trash, link_document_multiple_clear_transformations,
    link_document_multiple_download, link_document_multiple_restore,
    link_document_multiple_update_page_count,
    link_document_page_navigation_first, link_document_page_navigation_last,
    link_document_page_navigation_next, link_document_page_navigation_previous,
    link_document_page_return, link_document_page_rotate_left,
    link_document_page_rotate_right, link_document_page_view,
    link_document_page_view_reset, link_document_page_zoom_in,
    link_document_page_zoom_out, link_document_pages, link_document_preview,
    link_document_print, link_document_properties, link_document_restore,
    link_document_trash, link_document_type_create, link_document_type_delete,
    link_document_type_edit, link_document_type_filename_create,
    link_document_type_filename_delete, link_document_type_filename_edit,
    link_document_type_filename_list, link_document_type_list,
    link_document_type_setup, link_document_update_page_count,
    link_document_version_download, link_document_version_list,
    link_document_version_revert, link_trash_can_empty
)
from .literals import (
    CHECK_DELETE_PERIOD_INTERVAL, CHECK_TRASH_PERIOD_INTERVAL,
    DELETE_STALE_STUBS_INTERVAL
)
from .models import (
    DeletedDocument, Document, DocumentPage, DocumentType,
    DocumentTypeFilename, DocumentVersion
)
from .permissions import (
    permission_document_delete, permission_document_download,
    permission_document_edit, permission_document_new_version,
    permission_document_print, permission_document_properties_edit,
    permission_document_trash, permission_document_version_revert,
    permission_document_view
)
from .settings import setting_thumbnail_size
from .statistics import (
    new_documents_per_month, new_document_pages_per_month,
    new_document_versions_per_month, total_document_per_month,
    total_document_page_per_month, total_document_version_per_month
)
from .widgets import document_thumbnail


class DocumentsApp(MayanAppConfig):
    name = 'documents'
    test = True
    verbose_name = _('Documents')

    def ready(self):
        super(DocumentsApp, self).ready()

        APIEndPoint(app=self, version_string='1')

        MissingItem(
            label=_('Create a document type'),
            description=_(
                'Every uploaded document must be assigned a document type, '
                'it is the basic way Mayan EDMS categorizes documents.'
            ), condition=lambda: not DocumentType.objects.exists(),
            view='documents:document_type_list'
        )

        ModelAttribute(
            Document, label=_('Label'), name='label', type_name='field'
        )

        ModelAttribute(
            Document,
            description=_('The MIME type of any of the versions of a document'),
            label=_('MIME type'), name='versions__mimetype', type_name='field'
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_document_delete, permission_document_download,
                permission_document_edit, permission_document_new_version,
                permission_document_print, permission_document_properties_edit,
                permission_document_trash, permission_document_version_revert,
                permission_document_view, permission_events_view,
                permission_transformation_create,
                permission_transformation_delete,
                permission_transformation_edit, permission_transformation_view,
            )
        )

        ModelPermission.register_proxy(
            source=Document, model=DocumentType,
        )

        ModelPermission.register_inheritance(
            model=Document, related='document_type',
        )

        ModelPermission.register_inheritance(
            model=DocumentVersion, related='document',
        )

        ModelPermission.register_inheritance(
            model=DocumentPage, related='document',
        )

        SourceColumn(
            source=Document, label=_('Thumbnail'),
            func=lambda context: document_thumbnail(
                context['object'], gallery_name='documents:document_list',
                size=setting_thumbnail_size.value,
                title=getattr(context['object'], 'label', None),
            )
        )
        SourceColumn(
            source=Document, label=_('Type'), attribute='document_type'
        )

        SourceColumn(
            source=DocumentType, label=_('Documents'),
            func=lambda context: context['object'].get_document_count(
                user=context['request'].user
            )
        )

        SourceColumn(
            source=DocumentTypeFilename, label=_('Enabled'),
            func=lambda context: two_state_template(context['object'].enabled)
        )

        SourceColumn(
            source=DeletedDocument, label=_('Thumbnail'),
            func=lambda context: document_thumbnail(
                context['object'],
                gallery_name='documents:delete_document_list',
                size=setting_thumbnail_size.value,
                title=getattr(context['object'], 'label', None),
                disable_title_link=True
            )
        )
        SourceColumn(
            source=DeletedDocument, label=_('Type'), attribute='document_type'
        )
        SourceColumn(
            source=DeletedDocument, label=_('Date time trashed'),
            attribute='deleted_date_time'
        )

        SourceColumn(
            source=DocumentVersion, label=_('Time and date'),
            attribute='timestamp'
        )
        SourceColumn(
            source=DocumentVersion, label=_('MIME type'),
            attribute='mimetype'
        )
        SourceColumn(
            source=DocumentVersion, label=_('Encoding'),
            attribute='encoding'
        )
        SourceColumn(
            source=DocumentVersion, label=_('Comment'),
            attribute='comment'
        )

        app.conf.CELERYBEAT_SCHEDULE.update(
            {
                'task_check_delete_periods': {
                    'task': 'documents.tasks.task_check_delete_periods',
                    'schedule': timedelta(
                        seconds=CHECK_DELETE_PERIOD_INTERVAL
                    ),
                },
                'task_check_trash_periods': {
                    'task': 'documents.tasks.task_check_trash_periods',
                    'schedule': timedelta(seconds=CHECK_TRASH_PERIOD_INTERVAL),
                },
                'task_delete_stubs': {
                    'task': 'documents.tasks.task_delete_stubs',
                    'schedule': timedelta(seconds=DELETE_STALE_STUBS_INTERVAL),
                },
            }
        )

        app.conf.CELERY_QUEUES.extend(
            (
                Queue(
                    'converter', Exchange('converter'),
                    routing_key='converter', delivery_mode=1
                ),
                Queue(
                    'documents_periodic', Exchange('documents_periodic'),
                    routing_key='documents_periodic', delivery_mode=1
                ),
                Queue('uploads', Exchange('uploads'), routing_key='uploads'),
            )
        )

        app.conf.CELERY_ROUTES.update(
            {
                'documents.tasks.task_check_delete_periods': {
                    'queue': 'documents_periodic'
                },
                'documents.tasks.task_check_trash_periods': {
                    'queue': 'documents_periodic'
                },
                'documents.tasks.task_delete_stubs': {
                    'queue': 'documents_periodic'
                },
                'documents.tasks.task_clear_image_cache': {
                    'queue': 'tools'
                },
                'documents.tasks.task_get_document_page_image': {
                    'queue': 'converter'
                },
                'documents.tasks.task_update_page_count': {
                    'queue': 'uploads'
                },
                'documents.tasks.task_upload_new_version': {
                    'queue': 'uploads'
                },
            }
        )

        menu_front_page.bind_links(
            links=(
                link_document_list_recent, link_document_list,
                link_document_list_deleted
            )
        )
        menu_setup.bind_links(links=(link_document_type_setup,))
        menu_tools.bind_links(links=(link_clear_image_cache,))

        # Document type links
        menu_object.bind_links(
            links=(
                link_document_type_edit, link_document_type_filename_list,
                link_acl_list, link_document_type_delete
            ), sources=(DocumentType,)
        )
        menu_object.bind_links(
            links=(
                link_document_type_filename_edit,
                link_document_type_filename_delete
            ), sources=(DocumentTypeFilename,)
        )
        menu_secondary.bind_links(
            links=(link_document_type_list, link_document_type_create),
            sources=(
                DocumentType, 'documents:document_type_create',
                'documents:document_type_list'
            )
        )
        menu_sidebar.bind_links(
            links=(link_document_type_filename_create,),
            sources=(
                DocumentTypeFilename, 'documents:document_type_filename_list',
                'documents:document_type_filename_create'
            )
        )
        menu_sidebar.bind_links(
            links=(link_trash_can_empty,),
            sources=(
                'documents:document_list_deleted', 'documents:trash_can_empty'
            )
        )

        # Document object links
        menu_object.bind_links(
            links=(
                link_document_edit, link_document_document_type_edit,
                link_document_print, link_document_trash,
                link_document_download, link_document_clear_transformations,
                link_document_update_page_count
            ), sources=(Document,)
        )
        menu_object.bind_links(
            links=(link_document_restore, link_document_delete),
            sources=(DeletedDocument,)
        )

        # Document facet links
        menu_facet.bind_links(links=(link_acl_list,), sources=(Document,))
        menu_facet.bind_links(
            links=(link_document_preview,), sources=(Document,), position=0
        )
        menu_facet.bind_links(
            links=(link_document_properties,), sources=(Document,), position=2
        )
        menu_facet.bind_links(
            links=(link_events_for_object, link_document_version_list,),
            sources=(Document,), position=2
        )
        menu_facet.bind_links(links=(link_document_pages,), sources=(Document,))

        # Document actions
        menu_object.bind_links(
            links=(
                link_document_version_revert, link_document_version_download
            ),
            sources=(DocumentVersion,)
        )
        menu_multi_item.bind_links(
            links=(
                link_document_multiple_clear_transformations,
                link_document_multiple_trash, link_document_multiple_download,
                link_document_multiple_update_page_count,
                link_document_multiple_document_type_edit
            ), sources=(Document,)
        )
        menu_multi_item.bind_links(
            links=(
                link_document_multiple_restore, link_document_multiple_delete
            ), sources=(DeletedDocument,)
        )

        # Document pages
        menu_facet.bind_links(
            links=(
                link_document_page_rotate_left,
                link_document_page_rotate_right, link_document_page_zoom_in,
                link_document_page_zoom_out, link_document_page_view_reset
            ), sources=('documents:document_page_view',)
        )
        menu_facet.bind_links(
            links=(link_document_page_return, link_document_page_view),
            sources=(DocumentPage,)
        )
        menu_facet.bind_links(
            links=(
                link_document_page_navigation_first,
                link_document_page_navigation_previous,
                link_document_page_navigation_next,
                link_document_page_navigation_last, link_transformation_list
            ), sources=(DocumentPage,)
        )
        menu_object.bind_links(
            links=(link_transformation_list,), sources=(DocumentPage,)
        )

        namespace = StatisticNamespace(slug='documents', label=_('Documents'))
        namespace.add_statistic(
            slug='new-documents-per-month',
            label=_('New documents per month'),
            func=new_documents_per_month,
            renderer=CharJSLine,
            minute='0'
        )
        namespace.add_statistic(
            slug='new-document-versions-per-month',
            label=_('New document versions per month'),
            func=new_document_versions_per_month,
            renderer=CharJSLine,
            minute='0'
        )
        namespace.add_statistic(
            slug='new-document-pages-per-month',
            label=_('New document pages per month'),
            func=new_document_pages_per_month,
            renderer=CharJSLine,
            minute='0'
        )
        namespace.add_statistic(
            slug='total-documents-at-each-month',
            label=_('Total documents at each month'),
            func=total_document_per_month,
            renderer=CharJSLine,
            minute='0'
        )
        namespace.add_statistic(
            slug='total-document-versions-at-each-month',
            label=_('Total document versions at each month'),
            func=total_document_version_per_month,
            renderer=CharJSLine,
            minute='0'
        )
        namespace.add_statistic(
            slug='total-document-pages-at-each-month',
            label=_('Total document pages at each month'),
            func=total_document_page_per_month,
            renderer=CharJSLine,
            minute='0'
        )

        post_initial_setup.connect(
            create_default_document_type,
            dispatch_uid='create_default_document_type'
        )

        registry.register(DeletedDocument)
        registry.register(Document)
