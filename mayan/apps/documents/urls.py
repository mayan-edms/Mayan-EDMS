from django.conf.urls import url

from .api_views import (
    APITrashedDocumentListView, APIDeletedDocumentRestoreView,
    APIDeletedDocumentView, APIdocument_file,
    APIDocumentDownloadView, APIDocumentView, APIDocumentListView,
    APIDocumentFileDownloadView, APIDocumentFilePageImageView,
    APIDocumentFilePageView, APIDocumentTypeDocumentListView,
    APIDocumentTypeListView, APIDocumentTypeView,
    APIDocumentFilesListView, APIDocumentFilePageListView,
    APIDocumentFileView, APIRecentDocumentListView,
    APIDocumentVersionPageImageView
)
from .views.document_file_views import (
    DocumentFileDeleteView, DocumentFileDownloadView, DocumentFileListView,
    DocumentFilePropertiesView, DocumentFilePreviewView
)
from .views.document_file_page_views import (
    DocumentFilePageCountUpdateView, DocumentFilePageListView,
    DocumentFilePageNavigationFirst, DocumentFilePageNavigationLast,
    DocumentFilePageNavigationNext, DocumentFilePageNavigationPrevious,
    DocumentFilePageRotateLeftView, DocumentFilePageRotateRightView,
    DocumentFilePageView, DocumentFilePageViewResetView,
    DocumentFilePageZoomInView, DocumentFilePageZoomOutView
)
from .views.document_type_views import (
    DocumentTypeCreateView, DocumentTypeDeleteView,
    DocumentTypeDeletionPoliciesEditView, DocumentTypeDocumentListView,
    DocumentTypeEditView, DocumentTypeFileGeneratorEditView,
    DocumentTypeFilenameCreateView, DocumentTypeFilenameDeleteView,
    DocumentTypeFilenameEditView, DocumentTypeFilenameListView,
    DocumentTypeListView
)
from .views.document_version_page_views import (
    DocumentVersionPageDeleteView, DocumentVersionPageListView,
    DocumentVersionPageListRemapView, DocumentVersionPageListResetView,
    DocumentVersionPageNavigationFirst, DocumentVersionPageNavigationLast,
    DocumentVersionPageNavigationNext, DocumentVersionPageNavigationPrevious,
    DocumentVersionPageRotateLeftView, DocumentVersionPageRotateRightView,
    DocumentVersionPageView, DocumentVersionPageViewResetView,
    DocumentVersionPageView, DocumentVersionPageZoomInView,
    DocumentVersionPageZoomOutView
)
from .views.document_version_views import (
    DocumentVersionCreateView, DocumentVersionDeleteView,
    DocumentVersionEditView, DocumentVersionExportView,
    DocumentVersionListView, DocumentVersionPreviewView
)
from .views.document_views import (
    DocumentDocumentTypeChangeView, DocumentListView, DocumentPreviewView,
    DocumentPrint, DocumentPropertiesEditView,
    DocumentTransformationsClearView, DocumentTransformationsCloneView,
    DocumentView, RecentAccessDocumentListView, RecentAddedDocumentListView
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

urlpatterns_document_files = [
    url(
        regex=r'^documents/(?P<document_id>\d+)/files/$',
        name='document_file_list', view=DocumentFileListView.as_view()
    ),
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/preview/$',
        name='document_file_preview', view=DocumentFilePreviewView.as_view()
    ),
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/delete/$',
        name='document_file_delete',
        view=DocumentFileDeleteView.as_view()
    ),
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/download/$',
        name='document_file_download',
        view=DocumentFileDownloadView.as_view()
    ),
    #url(
    #    regex=r'^documents/files/(?P<document_file_id>\d+)/download/form/$',
    #    name='document_file_download_form',
    #    view=DocumentFileDownloadFormView.as_view()
    #),
    #url(
    #    regex=r'^documents/files/multiple/download/$',
    #    name='document_file_multiple_download',
    #    view=DocumentFileDownloadView.as_view()
    #),
    #url(
    #    regex=r'^documents/files/multiple/download/form/$',
    #    name='document_file_multiple_download_form',
    #    view=DocumentFileDownloadFormView.as_view()
    #),
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/properties/$',
        name='document_file_properties',
        view=DocumentFilePropertiesView.as_view()
    ),
]

urlpatterns_document_file_pages = [
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/pages/$',
        name='document_file_page_list', view=DocumentFilePageListView.as_view()
    ),
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/pages/update/$',
        name='document_file_page_count_update',
        view=DocumentFilePageCountUpdateView.as_view()
    ),
    url(
        regex=r'^documents/multiple/page/update/$',
        name='document_file_multiple_page_count_update',
        view=DocumentFilePageCountUpdateView.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_file_page_id>\d+)/$',
        name='document_file_page_view', view=DocumentFilePageView.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_file_page_id>\d+)/navigation/next/$',
        name='document_file_page_navigation_next',
        view=DocumentFilePageNavigationNext.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_file_page_id>\d+)/navigation/previous/$',
        name='document_file_page_navigation_previous',
        view=DocumentFilePageNavigationPrevious.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_file_page_id>\d+)/navigation/first/$',
        name='document_file_page_navigation_first',
        view=DocumentFilePageNavigationFirst.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_file_page_id>\d+)/navigation/last/$',
        name='document_file_page_navigation_last',
        view=DocumentFilePageNavigationLast.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_file_page_id>\d+)/zoom/in/$',
        name='document_file_page_zoom_in', view=DocumentFilePageZoomInView.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_file_page_id>\d+)/zoom/out/$',
        name='document_file_page_zoom_out', view=DocumentFilePageZoomOutView.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_file_page_id>\d+)/rotate/left/$',
        name='document_file_page_rotate_left',
        view=DocumentFilePageRotateLeftView.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_file_page_id>\d+)/rotate/right/$',
        name='document_file_page_rotate_right',
        view=DocumentFilePageRotateRightView.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_file_page_id>\d+)/reset/$',
        name='document_file_page_view_reset',
        view=DocumentFilePageViewResetView.as_view()
    ),
]

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
        regex=r'^document_types/(?P<document_type_id>\d+)/filename_generator/$',
        name='document_type_filename_generator',
        view=DocumentTypeFileGeneratorEditView.as_view()
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

urlpatterns_document_version = [
    url(
        regex=r'^documents/(?P<document_id>\d+)/versions/$',
        name='document_version_list', view=DocumentVersionListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/versions/create/$',
        name='document_version_create',
        view=DocumentVersionCreateView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/delete/$',
        name='document_version_delete',
        view=DocumentVersionDeleteView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/export/$',
        name='document_version_export',
        view=DocumentVersionExportView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/edit/$',
        name='document_version_edit',
        view=DocumentVersionEditView.as_view()
    ),
    url(
        regex=r'^documents/versions/multiple/delete/$',
        name='document_version_multiple_delete',
        view=DocumentVersionDeleteView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/preview/$',
        name='document_version_preview',
        view=DocumentVersionPreviewView.as_view()
    ),
]

urlpatterns_document_version_pages = [
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/pages/$',
        name='document_version_page_list',
        view=DocumentVersionPageListView.as_view()
    ),
    url(
        regex=r'^documents/versions/pages/(?P<document_version_page_id>\d+)/delete/$',
        name='document_version_page_delete',
        view=DocumentVersionPageDeleteView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/pages/remap/$',
        name='document_version_page_list_remap',
        view=DocumentVersionPageListRemapView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/pages/reset/$',
        name='document_version_page_list_reset',
        view=DocumentVersionPageListResetView.as_view()
    ),
    url(
        regex=r'^documents/versions/pages/(?P<document_version_page_id>\d+)/$',
        name='document_version_page_view',
        view=DocumentVersionPageView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_page_id>\d+)/navigation/next/$',
        name='document_version_page_navigation_next',
        view=DocumentVersionPageNavigationNext.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_page_id>\d+)/navigation/previous/$',
        name='document_version_page_navigation_previous',
        view=DocumentVersionPageNavigationPrevious.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_page_id>\d+)/navigation/first/$',
        name='document_version_page_navigation_first',
        view=DocumentVersionPageNavigationFirst.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_page_id>\d+)/navigation/last/$',
        name='document_version_page_navigation_last',
        view=DocumentVersionPageNavigationLast.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_page_id>\d+)/zoom/in/$',
        name='document_version_page_zoom_in', view=DocumentVersionPageZoomInView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_page_id>\d+)/zoom/out/$',
        name='document_version_page_zoom_out', view=DocumentVersionPageZoomOutView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_page_id>\d+)/rotate/left/$',
        name='document_version_page_rotate_left',
        view=DocumentVersionPageRotateLeftView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_page_id>\d+)/rotate/right/$',
        name='document_version_page_rotate_right',
        view=DocumentVersionPageRotateRightView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_page_id>\d+)/reset/$',
        name='document_version_page_view_reset',
        view=DocumentVersionPageViewResetView.as_view()
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
        view=DocumentDocumentTypeChangeView.as_view()
    ),
    url(
        regex=r'^documents/multiple/type/$',
        name='document_multiple_document_type_edit',
        view=DocumentDocumentTypeChangeView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/print/$',
        name='document_print', view=DocumentPrint.as_view()
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
urlpatterns.extend(urlpatterns_document_files)
urlpatterns.extend(urlpatterns_document_file_pages)
urlpatterns.extend(urlpatterns_document_types)
urlpatterns.extend(urlpatterns_document_version_pages)
urlpatterns.extend(urlpatterns_document_version)
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
        view=APIdocument_file.as_view(),
        name='document-type-change'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/files/$',
        view=APIDocumentFilesListView.as_view(),
        name='documentfile-list'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/files/(?P<file_pk>[0-9]+)/$',
        view=APIDocumentFileView.as_view(), name='documentfile-detail'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/files/(?P<file_pk>[0-9]+)/download/$',
        view=APIDocumentFileDownloadView.as_view(),
        name='documentfile-download'
    ),
    url(
        regex=r'^documents/recent/$', view=APIRecentDocumentListView.as_view(),
        name='document-recent-list'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/files/(?P<file_pk>[0-9]+)/pages/$',
        view=APIDocumentFilePageListView.as_view(),
        name='documentfilepage-list'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/files/(?P<file_pk>[0-9]+)/pages/(?P<page_pk>[0-9]+)$',
        view=APIDocumentFilePageView.as_view(), name='documentfilepage-detail'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/files/(?P<file_pk>[0-9]+)/pages/(?P<page_pk>[0-9]+)/image/$',
        view=APIDocumentFilePageImageView.as_view(), name='documentfilepage-image'
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/versions/(?P<document_version_id>[0-9]+)/pages/(?P<document_version_page_id>[0-9]+)/image/$',
        view=APIDocumentVersionPageImageView.as_view(), name='documentversionpage-image'
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
