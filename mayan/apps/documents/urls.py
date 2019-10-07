from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APITrashedDocumentListView, APIDeletedDocumentRestoreView,
    APIDeletedDocumentView, APIDocumentDownloadView, APIDocumentView,
    APIDocumentListView, APIDocumentVersionDownloadView,
    APIDocumentPageImageView, APIDocumentPageView,
    APIDocumentTypeDocumentListView, APIDocumentTypeListView,
    APIDocumentTypeView, APIDocumentVersionsListView,
    APIDocumentVersionPageListView, APIDocumentVersionView,
    APIRecentDocumentListView
)
from .views.document_views import (
    DocumentDocumentTypeEditView, DocumentDownloadFormView,
    DocumentDownloadView, DocumentDuplicatesListView, DocumentEditView,
    DocumentListView, DocumentPreviewView, DocumentPrint,
    DocumentTransformationsClearView, DocumentTransformationsCloneView,
    DocumentUpdatePageCountView, DocumentView, DuplicatedDocumentListView,
    RecentAccessDocumentListView, RecentAddedDocumentListView
)
from .views.document_page_views import (
    DocumentPageDisable, DocumentPageEnable, DocumentPageListView,
    DocumentPageNavigationFirst, DocumentPageNavigationLast,
    DocumentPageNavigationNext, DocumentPageNavigationPrevious,
    DocumentPageRotateLeftView, DocumentPageRotateRightView,
    DocumentPageView, DocumentPageViewResetView, DocumentPageZoomInView,
    DocumentPageZoomOutView
)
from .views.document_version_views import (
    DocumentVersionDownloadFormView, DocumentVersionDownloadView,
    DocumentVersionListView, DocumentVersionRevertView, DocumentVersionView,
)
from .views.document_type_views import (
    DocumentTypeCreateView, DocumentTypeDeleteView,
    DocumentTypeDeletionPoliciesEditView, DocumentTypeDocumentListView,
    DocumentTypeEditView, DocumentTypeFilenameCreateView,
    DocumentTypeFilenameDeleteView, DocumentTypeFilenameEditView,
    DocumentTypeFilenameListView, DocumentTypeListView
)
from .views.favorite_document_views import (
    FavoriteAddView, FavoriteDocumentListView, FavoriteRemoveView
)
from .views.misc_views import ScanDuplicatedDocuments
from .views.trashed_document_views import (
    DocumentTrashView, EmptyTrashCanView, TrashedDocumentDeleteView,
    TrashedDocumentListView, TrashedDocumentRestoreView
)

urlpatterns_document_types = [
    url(
        regex=r'^document_types/$', view=DocumentTypeListView.as_view(),
        name='document_type_list'
    ),
    url(
        regex=r'^document_types/create/$', view=DocumentTypeCreateView.as_view(),
        name='document_type_create'
    ),
    url(
        regex=r'^document_types/(?P<pk>\d+)/delete/$',
        view=DocumentTypeDeleteView.as_view(), name='document_type_delete'
    ),
    url(
        regex=r'^document_types/(?P<pk>\d+)/edit/$', view=DocumentTypeEditView.as_view(),
        name='document_type_edit'
    ),
    url(
        regex=r'^document_types/(?P<pk>\d+)/documents/$',
        view=DocumentTypeDocumentListView.as_view(),
        name='document_type_document_list'
    ),
    url(
        regex=r'^document_types/(?P<pk>\d+)/filenames/$',
        view=DocumentTypeFilenameListView.as_view(),
        name='document_type_filename_list'
    ),
    url(
        regex=r'^document_types/filenames/(?P<pk>\d+)/delete/$',
        view=DocumentTypeFilenameDeleteView.as_view(),
        name='document_type_filename_delete'
    ),
    url(
        regex=r'^document_types/filenames/(?P<pk>\d+)/edit/$',
        view=DocumentTypeFilenameEditView.as_view(),
        name='document_type_filename_edit'
    ),
    url(
        regex=r'^document_types/(?P<pk>\d+)/filenames/create/$',
        view=DocumentTypeFilenameCreateView.as_view(),
        name='document_type_filename_create'
    ),
    url(
        regex=r'^document_types/(?P<pk>\d+)/deletion_policies/$',
        view=DocumentTypeDeletionPoliciesEditView.as_view(),
        name='document_type_policies'
    ),
]

urlpatterns_favorite_documents = [
    url(
        regex=r'^documents/favorites/$', view=FavoriteDocumentListView.as_view(),
        name='document_list_favorites'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/add_to_favorites/$',
        view=FavoriteAddView.as_view(), name='document_add_to_favorites'
    ),
    url(
        regex=r'^documents/multiple/add_to_favorites/$', view=FavoriteAddView.as_view(),
        name='document_multiple_add_to_favorites'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/remove_from_favorites/$',
        view=FavoriteRemoveView.as_view(),
        name='document_remove_from_favorites'
    ),
    url(
        regex=r'^documents/multiple/remove_from_favorites/$',
        view=FavoriteRemoveView.as_view(),
        name='document_multiple_remove_from_favorites'
    ),
]

urlpatterns_documents = [
    url(
        regex=r'^documents/$', view=DocumentListView.as_view(), name='document_list'
    ),
    url(
        regex=r'^documents/recent_access/$',
        view=RecentAccessDocumentListView.as_view(),
        name='document_list_recent_access'
    ),
    url(
        regex=r'^documents/recent_added/$',
        view=RecentAddedDocumentListView.as_view(),
        name='document_list_recent_added'
    ),
    url(
        regex=r'^documents/duplicated/$',
        view=DuplicatedDocumentListView.as_view(),
        name='duplicated_document_list'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/preview/$', view=DocumentPreviewView.as_view(),
        name='document_preview'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/properties/$', view=DocumentView.as_view(),
        name='document_properties'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/duplicates/$',
        view=DocumentDuplicatesListView.as_view(),
        name='document_duplicates_list'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/type/$',
        view=DocumentDocumentTypeEditView.as_view(),
        name='document_document_type_edit'
    ),
    url(
        regex=r'^documents/multiple/type/$', view=DocumentDocumentTypeEditView.as_view(),
        name='document_multiple_document_type_edit'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/edit/$', view=DocumentEditView.as_view(),
        name='document_edit'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/print/$', view=DocumentPrint.as_view(),
        name='document_print'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/reset_page_count/$',
        view=DocumentUpdatePageCountView.as_view(),
        name='document_update_page_count'
    ),
    url(
        regex=r'^documents/multiple/reset_page_count/$',
        view=DocumentUpdatePageCountView.as_view(),
        name='document_multiple_update_page_count'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/download/form/$',
        view=DocumentDownloadFormView.as_view(), name='document_download_form'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/download/$', view=DocumentDownloadView.as_view(),
        name='document_download'
    ),
    url(
        regex=r'^documents/multiple/download/form/$',
        view=DocumentDownloadFormView.as_view(),
        name='document_multiple_download_form'
    ),
    url(
        regex=r'^documents/multiple/download/$', view=DocumentDownloadView.as_view(),
        name='document_multiple_download'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/transformations/clear/$',
        view=DocumentTransformationsClearView.as_view(),
        name='document_clear_transformations'
    ),
    url(
        regex=r'^documents/multiple/clear_transformations/$',
        view=DocumentTransformationsClearView.as_view(),
        name='document_multiple_clear_transformations'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/transformations/clone/$',
        view=DocumentTransformationsCloneView.as_view(),
        name='document_clone_transformations'
    ),
]

urlpatterns_document_pages = [
    url(
        regex=r'^documents/(?P<pk>\d+)/pages/$', view=DocumentPageListView.as_view(),
        name='document_pages'
    ),
    url(
        regex=r'^documents/pages/(?P<pk>\d+)/$', view=DocumentPageView.as_view(),
        name='document_page_view'
    ),
    url(
        regex=r'^documents/pages/(?P<pk>\d+)/disable/$',
        name='document_page_disable', view=DocumentPageDisable.as_view()
    ),
    url(
        regex=r'^documents/pages/multiple/disable/$', name='document_page_multiple_disable',
        view=DocumentPageDisable.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<pk>\d+)/enable/$',
        name='document_page_enable', view=DocumentPageEnable.as_view()
    ),
    url(
        regex=r'^documents/pages/multiple/enable/$', name='document_page_multiple_enable',
        view=DocumentPageEnable.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<pk>\d+)/navigation/next/$',
        view=DocumentPageNavigationNext.as_view(),
        name='document_page_navigation_next'
    ),
    url(
        regex=r'^documents/pages/(?P<pk>\d+)/navigation/previous/$',
        view=DocumentPageNavigationPrevious.as_view(),
        name='document_page_navigation_previous'
    ),
    url(
        regex=r'^documents/pages/(?P<pk>\d+)/navigation/first/$',
        view=DocumentPageNavigationFirst.as_view(),
        name='document_page_navigation_first'
    ),
    url(
        regex=r'^documents/pages/(?P<pk>\d+)/navigation/last/$',
        view=DocumentPageNavigationLast.as_view(),
        name='document_page_navigation_last'
    ),
    url(
        regex=r'^documents/pages/(?P<pk>\d+)/zoom/in/$',
        view=DocumentPageZoomInView.as_view(), name='document_page_zoom_in'
    ),
    url(
        regex=r'^documents/pages/(?P<pk>\d+)/zoom/out/$',
        view=DocumentPageZoomOutView.as_view(), name='document_page_zoom_out'
    ),
    url(
        regex=r'^documents/pages/(?P<pk>\d+)/rotate/left/$',
        view=DocumentPageRotateLeftView.as_view(),
        name='document_page_rotate_left'
    ),
    url(
        regex=r'^documents/pages/(?P<pk>\d+)/rotate/right/$',
        view=DocumentPageRotateRightView.as_view(),
        name='document_page_rotate_right'
    ),
    url(
        regex=r'^documents/pages/(?P<pk>\d+)/reset/$',
        view=DocumentPageViewResetView.as_view(),
        name='document_page_view_reset'
    ),
]

urlpatterns_document_versions = [
    url(
        regex=r'^documents/(?P<pk>\d+)/versions/$',
        view=DocumentVersionListView.as_view(),
        name='document_version_list'
    ),
    url(
        regex=r'^documents/versions/(?P<pk>\d+)/download/form/$',
        view=DocumentVersionDownloadFormView.as_view(),
        name='document_version_download_form'
    ),
    url(
        regex=r'^documents/versions/(?P<pk>\d+)/$',
        view=DocumentVersionView.as_view(), name='document_version_view'
    ),
    url(
        regex=r'^documents/versions/(?P<pk>\d+)/download/$',
        view=DocumentVersionDownloadView.as_view(),
        name='document_version_download'
    ),
    url(
        regex=r'^documents/versions/(?P<pk>\d+)/revert/$',
        view=DocumentVersionRevertView.as_view(),
        name='document_version_revert'
    ),
]

urlpatterns_tools = [
    url(
        regex=r'^tools/documents/duplicated/scan/$',
        view=ScanDuplicatedDocuments.as_view(),
        name='duplicated_document_scan'
    ),
]

urlpatterns_trashed_documents = [
    url(
        regex=r'^documents/(?P<pk>\d+)/trash/$', view=DocumentTrashView.as_view(),
        name='document_trash'
    ),
    url(
        regex=r'^documents/multiple/trash/$', view=DocumentTrashView.as_view(),
        name='document_multiple_trash'
    ),
    url(
        regex=r'^trashed_documents/$', view=TrashedDocumentListView.as_view(),
        name='document_list_deleted'
    ),
    url(
        regex=r'^trashed_documents/(?P<pk>\d+)/restore/$',
        view=TrashedDocumentRestoreView.as_view(), name='document_restore'
    ),
    url(
        regex=r'^trashed_documents/multiple/restore/$', view=TrashedDocumentRestoreView.as_view(),
        name='document_multiple_restore'
    ),
    url(
        regex=r'^trashed_documents/(?P<pk>\d+)/delete/$',
        view=TrashedDocumentDeleteView.as_view(), name='document_delete'
    ),
    url(
        regex=r'^trashed_documents/multiple/delete/$',
        view=TrashedDocumentDeleteView.as_view(),
        name='document_multiple_delete'
    ),
    url(
        regex=r'^trash_can/empty/$', view=EmptyTrashCanView.as_view(),
        name='trash_can_empty'
    ),
]

urlpatterns = []
urlpatterns.extend(urlpatterns_documents)
urlpatterns.extend(urlpatterns_document_pages)
urlpatterns.extend(urlpatterns_document_types)
urlpatterns.extend(urlpatterns_document_versions)
urlpatterns.extend(urlpatterns_favorite_documents)
urlpatterns.extend(urlpatterns_tools)
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
