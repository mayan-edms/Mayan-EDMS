from django.conf.urls import url

from .api_views.document_api_views import (
    APIDocumentDetailView, APIDocumentListView, APIDocumentChangeTypeView,
    APIDocumentUploadView
)
from .api_views.document_file_api_views import (
    APIDocumentFileDetailView, APIDocumentFileDownloadView,
    APIDocumentFileListView, APIDocumentFilePageImageView,
    APIDocumentFilePageDetailView, APIDocumentFilePageListView
)
from .api_views.document_type_api_views import (
    APIDocumentTypeDetailView, APIDocumentTypeListView,
    APIDocumentTypeQuickLabelDetailView, APIDocumentTypeQuickLabelListView
)
from .api_views.document_version_api_views import (
    APIDocumentVersionDetailView, APIDocumentVersionExportView,
    APIDocumentVersionListView, APIDocumentVersionPageDetailView,
    APIDocumentVersionPageImageView, APIDocumentVersionPageListView
)
from .api_views.favorite_document_api_views import (
    APIFavoriteDocumentDetailView, APIFavoriteDocumentListView
)
from .api_views.recently_accessed_document_api_views import (
    APIRecentlyAccessedDocumentListView
)
from .api_views.recently_created_document_api_views import (
    APIRecentlyCreatedDocumentListView
)
from .api_views.trashed_document_api_views import (
    APITrashedDocumentListView, APITrashedDocumentRestoreView,
    APITrashedDocumentDetailView
)
from .views.document_file_views import (
    DocumentFileDeleteView, DocumentFileDownloadView, DocumentFileEditView,
    DocumentFileListView, DocumentFilePrintFormView, DocumentFilePrintView,
    DocumentFilePropertiesView, DocumentFilePreviewView,
    DocumentFileTransformationsClearView,
    DocumentFileTransformationsCloneView
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
    DocumentVersionPageZoomInView, DocumentVersionPageZoomOutView
)
from .views.document_version_views import (
    DocumentVersionActiveView, DocumentVersionCreateView,
    DocumentVersionDeleteView, DocumentVersionEditView,
    DocumentVersionExportView, DocumentVersionListView,
    DocumentVersionPreviewView, DocumentVersionPrintFormView,
    DocumentVersionPrintView, DocumentVersionTransformationsClearView,
    DocumentVersionTransformationsCloneView
)
from .views.document_views import (
    DocumentTypeChangeView, DocumentListView, DocumentPreviewView,
    DocumentPropertiesEditView, DocumentPropertiesView
)
from .views.favorite_document_views import (
    FavoriteAddView, FavoriteDocumentListView, FavoriteRemoveView
)
from .views.recently_accessed_document_views import (
    RecentlyAccessedDocumentListView
)
from .views.recently_created_document_views import (
    RecentCreatedDocumentListView
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
        regex=r'^documents/files/multiple/delete/$',
        name='document_file_delete_multiple',
        view=DocumentFileDeleteView.as_view()
    ),
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/download/$',
        name='document_file_download',
        view=DocumentFileDownloadView.as_view()
    ),
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/edit/$',
        name='document_file_edit',
        view=DocumentFileEditView.as_view()
    ),
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/print/form/$',
        name='document_file_print_form',
        view=DocumentFilePrintFormView.as_view()
    ),
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/print/$',
        name='document_file_print_view', view=DocumentFilePrintView.as_view()
    ),
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/properties/$',
        name='document_file_properties',
        view=DocumentFilePropertiesView.as_view()
    ),
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/transformations/clear/$',
        name='document_file_transformations_clear',
        view=DocumentFileTransformationsClearView.as_view()
    ),
    url(
        regex=r'^documents/files/multiple/transformations/clear/$',
        name='document_file_multiple_transformations_clear',
        view=DocumentFileTransformationsClearView.as_view()
    ),
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/transformations/clone/$',
        name='document_file_transformations_clone',
        view=DocumentFileTransformationsCloneView.as_view()
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
        regex=r'^documents/files/multiple/page/update/$',
        name='document_file_multiple_page_count_update',
        view=DocumentFilePageCountUpdateView.as_view()
    ),
    url(
        regex=r'^documents/files/pages/(?P<document_file_page_id>\d+)/$',
        name='document_file_page_view', view=DocumentFilePageView.as_view()
    ),
    url(
        regex=r'^documents/files/pages/(?P<document_file_page_id>\d+)/navigation/next/$',
        name='document_file_page_navigation_next',
        view=DocumentFilePageNavigationNext.as_view()
    ),
    url(
        regex=r'^documents/files/pages/(?P<document_file_page_id>\d+)/navigation/previous/$',
        name='document_file_page_navigation_previous',
        view=DocumentFilePageNavigationPrevious.as_view()
    ),
    url(
        regex=r'^documents/files/pages/(?P<document_file_page_id>\d+)/navigation/first/$',
        name='document_file_page_navigation_first',
        view=DocumentFilePageNavigationFirst.as_view()
    ),
    url(
        regex=r'^documents/files/pages/(?P<document_file_page_id>\d+)/navigation/last/$',
        name='document_file_page_navigation_last',
        view=DocumentFilePageNavigationLast.as_view()
    ),
    url(
        regex=r'^documents/files/pages/(?P<document_file_page_id>\d+)/zoom/in/$',
        name='document_file_page_zoom_in', view=DocumentFilePageZoomInView.as_view()
    ),
    url(
        regex=r'^documents/files/pages/(?P<document_file_page_id>\d+)/zoom/out/$',
        name='document_file_page_zoom_out', view=DocumentFilePageZoomOutView.as_view()
    ),
    url(
        regex=r'^documents/files/pages/(?P<document_file_page_id>\d+)/rotate/left/$',
        name='document_file_page_rotate_left',
        view=DocumentFilePageRotateLeftView.as_view()
    ),
    url(
        regex=r'^documents/files/pages/(?P<document_file_page_id>\d+)/rotate/right/$',
        name='document_file_page_rotate_right',
        view=DocumentFilePageRotateRightView.as_view()
    ),
    url(
        regex=r'^documents/files/pages/(?P<document_file_page_id>\d+)/reset/$',
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
        regex=r'^documents/versions/(?P<document_version_id>\d+)/active/$',
        name='document_version_active',
        view=DocumentVersionActiveView.as_view()
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
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/print/form/$',
        name='document_version_print_form',
        view=DocumentVersionPrintFormView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/print/$',
        name='document_version_print_view',
        view=DocumentVersionPrintView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/transformations/clear/$',
        name='document_version_transformations_clear',
        view=DocumentVersionTransformationsClearView.as_view()
    ),
    url(
        regex=r'^documents/versions/multiple/transformations/clear/$',
        name='document_version_multiple_transformations_clear',
        view=DocumentVersionTransformationsClearView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/transformations/clone/$',
        name='document_version_transformations_clone',
        view=DocumentVersionTransformationsCloneView.as_view()
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
        regex=r'^documents/recently/accessed/$',
        name='document_recently_accessed_list',
        view=RecentlyAccessedDocumentListView.as_view()
    ),
    url(
        regex=r'^documents/recently/created/$',
        name='document_recently_created_list',
        view=RecentCreatedDocumentListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/preview/$',
        name='document_preview', view=DocumentPreviewView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/properties/$',
        name='document_properties', view=DocumentPropertiesView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/properties/edit/$',
        name='document_properties_edit',
        view=DocumentPropertiesEditView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/type/$',
        name='document_type_change',
        view=DocumentTypeChangeView.as_view()
    ),
    url(
        regex=r'^documents/multiple/type/$',
        name='document_multiple_type_change',
        view=DocumentTypeChangeView.as_view()
    ),
]

urlpatterns_favorite_documents = [
    url(
        regex=r'^documents/favorites/$', name='document_favorite_list',
        view=FavoriteDocumentListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/add_to_favorites/$',
        name='document_favorite_add', view=FavoriteAddView.as_view()
    ),
    url(
        regex=r'^documents/multiple/add_to_favorites/$',
        name='document_multiple_favorite_add', view=FavoriteAddView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/remove_from_favorites/$',
        name='document_favorite_remove', view=FavoriteRemoveView.as_view()
    ),
    url(
        regex=r'^documents/multiple/remove_from_favorites/$',
        name='document_multiple_favorite_remove',
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
urlpatterns.extend(urlpatterns_favorite_documents)
urlpatterns.extend(urlpatterns_trashed_documents)

api_urls_documents = [
    url(
        regex=r'^documents/$', name='document-list',
        view=APIDocumentListView.as_view()

    ),
    url(
        regex=r'^documents/upload/$', name='document-upload',
        view=APIDocumentUploadView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/$',
        name='document-detail',
        view=APIDocumentDetailView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/type/change/$',
        name='document-change-type', view=APIDocumentChangeTypeView.as_view()
    ),
    url(
        regex=r'^documents/accessed/$',
        name='recentlyaccesseddocument-list',
        view=APIRecentlyAccessedDocumentListView.as_view()
    ),
    url(
        regex=r'^documents/created/$',
        name='recentlycreateddocument-list',
        view=APIRecentlyCreatedDocumentListView.as_view()
    ),
    url(
        regex=r'^documents/favorites/$',
        name='favoritedocument-list',
        view=APIFavoriteDocumentListView.as_view()
    ),
    url(
        regex=r'^documents/favorites/(?P<favorite_document_id>[0-9]+)/$',
        name='favoritedocument-detail',
        view=APIFavoriteDocumentDetailView.as_view()
    )
]

api_urls_document_files = [
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/files/$',
        name='documentfile-list',
        view=APIDocumentFileListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/files/(?P<document_file_id>[0-9]+)/$',
        name='documentfile-detail', view=APIDocumentFileDetailView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/files/(?P<document_file_id>[0-9]+)/download/$',
        name='documentfile-download',
        view=APIDocumentFileDownloadView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/files/(?P<document_file_id>[0-9]+)/pages/$',
        name='documentfilepage-list',
        view=APIDocumentFilePageListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/files/(?P<document_file_id>[0-9]+)/pages/(?P<document_file_page_id>[0-9]+)/$',
        name='documentfilepage-detail',
        view=APIDocumentFilePageDetailView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/files/(?P<document_file_id>[0-9]+)/pages/(?P<document_file_page_id>[0-9]+)/image/$',
        name='documentfilepage-image',
        view=APIDocumentFilePageImageView.as_view()
    )
]

api_urls_document_types = [
    url(
        regex=r'^document_types/$', name='documenttype-list',
        view=APIDocumentTypeListView.as_view()
    ),
    url(
        regex=r'^document_types/(?P<document_type_id>[0-9]+)/$',
        name='documenttype-detail', view=APIDocumentTypeDetailView.as_view()
    ),
    url(
        regex=r'^document_types/(?P<document_type_id>[0-9]+)/quick_labels/$',
        name='documenttype-quicklabel-list',
        view=APIDocumentTypeQuickLabelListView.as_view()
    ),
    url(
        regex=r'^document_types/(?P<document_type_id>[0-9]+)/quick_labels/(?P<document_type_quick_label_id>[0-9]+)/$',
        name='documenttype-quicklabel-detail',
        view=APIDocumentTypeQuickLabelDetailView.as_view()
    )
]

api_urls_document_versions = [
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/versions/$',
        name='documentversion-list',
        view=APIDocumentVersionListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/versions/(?P<document_version_id>[0-9]+)/$',
        name='documentversion-detail',
        view=APIDocumentVersionDetailView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/versions/(?P<document_version_id>[0-9]+)/export/$',
        view=APIDocumentVersionExportView.as_view(),
        name='documentversion-export'
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/versions/(?P<document_version_id>[0-9]+)/pages/$',
        name='documentversionpage-list',
        view=APIDocumentVersionPageListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/versions/(?P<document_version_id>[0-9]+)/pages/(?P<document_version_page_id>[0-9]+)/$',
        name='documentversionpage-detail',
        view=APIDocumentVersionPageDetailView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/versions/(?P<document_version_id>[0-9]+)/pages/(?P<document_version_page_id>[0-9]+)/image/$',
        name='documentversionpage-image',
        view=APIDocumentVersionPageImageView.as_view()
    )
]

api_urls_trashed_documents = [
    url(
        regex=r'^trashed_documents/$', name='trasheddocument-list',
        view=APITrashedDocumentListView.as_view()
    ),
    url(
        regex=r'^trashed_documents/(?P<document_id>[0-9]+)/$',
        name='trasheddocument-detail', view=APITrashedDocumentDetailView.as_view()
    ),
    url(
        regex=r'^trashed_documents/(?P<document_id>[0-9]+)/restore/$',
        name='trasheddocument-restore',
        view=APITrashedDocumentRestoreView.as_view()
    ),
]

api_urls = []
api_urls.extend(api_urls_documents)
api_urls.extend(api_urls_document_files)
api_urls.extend(api_urls_document_versions)
api_urls.extend(api_urls_document_types)
api_urls.extend(api_urls_trashed_documents)
