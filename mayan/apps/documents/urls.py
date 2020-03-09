from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APITrashedDocumentListView, APIDeletedDocumentRestoreView,
    APIDeletedDocumentView, APIDocumentDocumentTypeChangeView,
    APIDocumentDownloadView, APIDocumentView, APIDocumentListView,
    APIDocumentVersionDownloadView, APIDocumentPageImageView,
    APIDocumentPageView, APIDocumentTypeDocumentListView,
    APIDocumentTypeListView, APIDocumentTypeView,
    APIDocumentVersionsListView, APIDocumentVersionPageListView,
    APIDocumentVersionView, APIRecentDocumentListView
)
from .views.document_page_views import (
    DocumentPageDisable, DocumentPageEnable, DocumentPageListView,
    DocumentPageNavigationFirst, DocumentPageNavigationLast,
    DocumentPageNavigationNext, DocumentPageNavigationPrevious,
    DocumentPageRotateLeftView, DocumentPageRotateRightView,
    DocumentPageView, DocumentPageViewResetView, DocumentPageZoomInView,
    DocumentPageZoomOutView
)
from .views.document_type_views import (
    DocumentTypeCreateView, DocumentTypeDeleteView,
    DocumentTypeDeletionPoliciesEditView, DocumentTypeDocumentListView,
    DocumentTypeEditView, DocumentTypeFilenameCreateView,
    DocumentTypeFilenameDeleteView, DocumentTypeFilenameEditView,
    DocumentTypeFilenameListView, DocumentTypeListView
)
from .views.document_version_views import (
    DocumentVersionDownloadFormView, DocumentVersionDownloadView,
    DocumentVersionListView, DocumentVersionRevertView, DocumentVersionView,
)
from .views.document_views import (
    DocumentDocumentTypeEditView, DocumentDownloadFormView,
    DocumentDownloadView, DocumentListView, DocumentPreviewView,
    DocumentPrint, DocumentPropertiesEditView,
    DocumentTransformationsClearView, DocumentTransformationsCloneView,
    DocumentUpdatePageCountView, DocumentView, RecentAccessDocumentListView,
    RecentAddedDocumentListView
)
from .views.duplicated_document_views import (
    DocumentDuplicatesListView, DuplicatedDocumentListView,
    ScanDuplicatedDocuments
)
from .views.favorite_document_views import (
    FavoriteAddView, FavoriteDocumentListView, FavoriteRemoveView
)
from .views.trashed_document_views import (
    DocumentTrashView, EmptyTrashCanView, TrashedDocumentDeleteView,
    TrashedDocumentListView, TrashedDocumentRestoreView
)

urlpatterns_document_types = [
    url(
        regex=r'^document_types/$', name='document_type_list',
        view=DocumentTypeListView.as_view()
    ),
    url(
        regex=r'^document_types/create/$', name='document_type_create',
        view=DocumentTypeCreateView.as_view()
    ),
    url(
        regex=r'^document_types/(?P<document_type_id>\d+)/delete/$',
        name='document_type_delete', view=DocumentTypeDeleteView.as_view()
    ),
    url(
        regex=r'^document_types/(?P<document_type_id>\d+)/deletion_policies/$',
        name='document_type_policies',
        view=DocumentTypeDeletionPoliciesEditView.as_view()
    ),
    url(
        regex=r'^document_types/(?P<document_type_id>\d+)/documents/$',
        name='document_type_document_list',
        view=DocumentTypeDocumentListView.as_view()
    ),
    url(
        regex=r'^document_types/(?P<document_type_id>\d+)/edit/$',
        name='document_type_edit', view=DocumentTypeEditView.as_view()
    ),
    url(
        regex=r'^document_types/(?P<document_type_id>\d+)/filenames/$',
        name='document_type_filename_list',
        view=DocumentTypeFilenameListView.as_view()
    ),
    url(
        regex=r'^document_types/(?P<document_type_id>\d+)/filenames/create/$',
        name='document_type_filename_create',
        view=DocumentTypeFilenameCreateView.as_view()
    ),
    url(
        regex=r'^document_types/filenames/(?P<document_type_filename_id>\d+)/delete/$',
        name='document_type_filename_delete',
        view=DocumentTypeFilenameDeleteView.as_view()
    ),
    url(
        regex=r'^document_types/filenames/(?P<document_type_filename_id>\d+)/edit/$',
        name='document_type_filename_edit',
        view=DocumentTypeFilenameEditView.as_view()
    ),
]

urlpatterns_documents = [
    url(
        regex=r'^documents/$', name='document_list',
        view=DocumentListView.as_view()
    ),
    url(
        regex=r'^documents/recent_access/$',
        name='document_list_recent_access',
        view=RecentAccessDocumentListView.as_view()
    ),
    url(
        regex=r'^documents/recent_added/$',
        name='document_list_recent_added',
        view=RecentAddedDocumentListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/preview/$',
        name='document_preview', view=DocumentPreviewView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/properties/$',
        name='document_properties', view=DocumentView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/properties/edit/$',
        name='document_edit', view=DocumentPropertiesEditView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/type/$',
        name='document_document_type_edit',
        view=DocumentDocumentTypeEditView.as_view()
    ),
    url(
        regex=r'^documents/multiple/type/$',
        name='document_multiple_document_type_edit',
        view=DocumentDocumentTypeEditView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/print/$',
        name='document_print', view=DocumentPrint.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/reset_page_count/$',
        name='document_update_page_count',
        view=DocumentUpdatePageCountView.as_view()
    ),
    url(
        regex=r'^documents/multiple/reset_page_count/$',
        name='document_multiple_update_page_count',
        view=DocumentUpdatePageCountView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/download/form/$',
        name='document_download_form',
        view=DocumentDownloadFormView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/download/$',
        name='document_download', view=DocumentDownloadView.as_view()
    ),
    url(
        regex=r'^documents/multiple/download/form/$',
        name='document_multiple_download_form',
        view=DocumentDownloadFormView.as_view()
    ),
    url(
        regex=r'^documents/multiple/download/$',
        name='document_multiple_download',
        view=DocumentDownloadView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/transformations/clear/$',
        name='document_clear_transformations',
        view=DocumentTransformationsClearView.as_view()
    ),
    url(
        regex=r'^documents/multiple/clear_transformations/$',
        name='document_multiple_clear_transformations',
        view=DocumentTransformationsClearView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/transformations/clone/$',
        name='document_clone_transformations',
        view=DocumentTransformationsCloneView.as_view()
    ),
]

urlpatterns_document_pages = [
    url(
        regex=r'^documents/(?P<document_id>\d+)/pages/$',
        name='document_pages', view=DocumentPageListView.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_page_id>\d+)/$',
        name='document_page_view', view=DocumentPageView.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_page_id>\d+)/disable/$',
        name='document_page_disable', view=DocumentPageDisable.as_view()
    ),
    url(
        regex=r'^documents/pages/multiple/disable/$',
        name='document_page_multiple_disable',
        view=DocumentPageDisable.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_page_id>\d+)/enable/$',
        name='document_page_enable', view=DocumentPageEnable.as_view()
    ),
    url(
        regex=r'^documents/pages/multiple/enable/$',
        name='document_page_multiple_enable',
        view=DocumentPageEnable.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_page_id>\d+)/navigation/next/$',
        name='document_page_navigation_next',
        view=DocumentPageNavigationNext.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_page_id>\d+)/navigation/previous/$',
        name='document_page_navigation_previous',
        view=DocumentPageNavigationPrevious.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_page_id>\d+)/navigation/first/$',
        name='document_page_navigation_first',
        view=DocumentPageNavigationFirst.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_page_id>\d+)/navigation/last/$',
        name='document_page_navigation_last',
        view=DocumentPageNavigationLast.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_page_id>\d+)/zoom/in/$',
        name='document_page_zoom_in', view=DocumentPageZoomInView.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_page_id>\d+)/zoom/out/$',
        name='document_page_zoom_out', view=DocumentPageZoomOutView.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_page_id>\d+)/rotate/left/$',
        name='document_page_rotate_left',
        view=DocumentPageRotateLeftView.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_page_id>\d+)/rotate/right/$',
        name='document_page_rotate_right',
        view=DocumentPageRotateRightView.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_page_id>\d+)/reset/$',
        name='document_page_view_reset',
        view=DocumentPageViewResetView.as_view()
    ),
]

urlpatterns_document_versions = [
    url(
        regex=r'^documents/(?P<document_id>\d+)/versions/$',
        name='document_version_list', view=DocumentVersionListView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/download/form/$',
        name='document_version_download_form',
        view=DocumentVersionDownloadFormView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/$',
        name='document_version_view', view=DocumentVersionView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/download/$',
        name='document_version_download',
        view=DocumentVersionDownloadView.as_view()
    ),
    url(
        regex=r'^documents/versions/multiple/download/$',
        name='document_multiple_version_download',
        view=DocumentVersionDownloadView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/revert/$',
        name='document_version_revert',
        view=DocumentVersionRevertView.as_view()
    ),
]

urlpatterns_duplicated_documents = [
    url(
        regex=r'^documents/duplicated/$',
        name='duplicated_document_list',
        view=DuplicatedDocumentListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/duplicates/$',
        name='document_duplicates_list',
        view=DocumentDuplicatesListView.as_view()
    ),
    url(
        regex=r'^tools/documents/duplicated/scan/$',
        name='duplicated_document_scan',
        view=ScanDuplicatedDocuments.as_view()
    ),
]

urlpatterns_favorite_documents = [
    url(
        regex=r'^documents/favorites/$', name='document_list_favorites',
        view=FavoriteDocumentListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/add_to_favorites/$',
        name='document_add_to_favorites', view=FavoriteAddView.as_view()
    ),
    url(
        regex=r'^documents/multiple/add_to_favorites/$',
        name='document_multiple_add_to_favorites',
        view=FavoriteAddView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/remove_from_favorites/$',
        name='document_remove_from_favorites',
        view=FavoriteRemoveView.as_view()
    ),
    url(
        regex=r'^documents/multiple/remove_from_favorites/$',
        name='document_multiple_remove_from_favorites',
        view=FavoriteRemoveView.as_view()
    ),
]

urlpatterns_trashed_documents = [
    url(
        regex=r'^documents/(?P<document_id>\d+)/trash/$',
        name='document_trash', view=DocumentTrashView.as_view()
    ),
    url(
        regex=r'^documents/multiple/trash/$', name='document_multiple_trash',
        view=DocumentTrashView.as_view()
    ),
    url(
        regex=r'^trashed_documents/$', name='document_list_deleted',
        view=TrashedDocumentListView.as_view()
    ),
    url(
        regex=r'^trashed_documents/(?P<document_id>\d+)/restore/$',
        name='document_restore', view=TrashedDocumentRestoreView.as_view()
    ),
    url(
        regex=r'^trashed_documents/multiple/restore/$',
        name='document_multiple_restore',
        view=TrashedDocumentRestoreView.as_view()
    ),
    url(
        regex=r'^trashed_documents/(?P<document_id>\d+)/delete/$',
        name='document_delete', view=TrashedDocumentDeleteView.as_view()
    ),
    url(
        regex=r'^trashed_documents/multiple/delete/$',
        name='document_multiple_delete',
        view=TrashedDocumentDeleteView.as_view()
    ),
    url(
        regex=r'^trash_can/empty/$', name='trash_can_empty',
        view=EmptyTrashCanView.as_view()
    ),
]

urlpatterns = []
urlpatterns.extend(urlpatterns_document_pages)
urlpatterns.extend(urlpatterns_document_types)
urlpatterns.extend(urlpatterns_document_versions)
urlpatterns.extend(urlpatterns_documents)
urlpatterns.extend(urlpatterns_duplicated_documents)
urlpatterns.extend(urlpatterns_favorite_documents)
urlpatterns.extend(urlpatterns_trashed_documents)

api_urls = [
    url(
        regex=r'^document_types/(?P<pk>[0-9]+)/$',
        view=APIDocumentTypeView.as_view(), name='documenttype-detail'
    ),
    url(
        regex=r'^document_types/$', view=APIDocumentTypeListView.as_view(),
        name='documenttype-list'
    ),
    url(
        regex=r'^document_types/(?P<pk>[0-9]+)/documents/$',
        view=APIDocumentTypeDocumentListView.as_view(),
        name='documenttype-document-list'
    ),
    url(
        regex=r'^documents/$', view=APIDocumentListView.as_view(),
        name='document-list'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/$', view=APIDocumentView.as_view(),
        name='document-detail'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/download/$',
        view=APIDocumentDownloadView.as_view(), name='document-download'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/type/change/$',
        view=APIDocumentDocumentTypeChangeView.as_view(),
        name='document-type-change'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/versions/$',
        view=APIDocumentVersionsListView.as_view(),
        name='document-version-list'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/versions/(?P<version_pk>[0-9]+)/$',
        view=APIDocumentVersionView.as_view(), name='documentversion-detail'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/versions/(?P<version_pk>[0-9]+)/pages/$',
        view=APIDocumentVersionPageListView.as_view(),
        name='documentversion-page-list'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/versions/(?P<version_pk>[0-9]+)/download/$',
        view=APIDocumentVersionDownloadView.as_view(),
        name='documentversion-download'
    ),
    url(
        regex=r'^documents/recent/$', view=APIRecentDocumentListView.as_view(),
        name='document-recent-list'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/versions/(?P<version_pk>[0-9]+)/pages/(?P<page_pk>[0-9]+)$',
        view=APIDocumentPageView.as_view(), name='documentpage-detail'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/versions/(?P<version_pk>[0-9]+)/pages/(?P<page_pk>[0-9]+)/image/$',
        view=APIDocumentPageImageView.as_view(), name='documentpage-image'
    ),
    url(
        regex=r'^trashed_documents/$',
        view=APITrashedDocumentListView.as_view(), name='trasheddocument-list'
    ),
    url(
        regex=r'^trashed_documents/(?P<pk>[0-9]+)/$',
        view=APIDeletedDocumentView.as_view(), name='trasheddocument-detail'
    ),
    url(
        regex=r'^trashed_documents/(?P<pk>[0-9]+)/restore/$',
        view=APIDeletedDocumentRestoreView.as_view(), name='trasheddocument-restore'
    ),
]
