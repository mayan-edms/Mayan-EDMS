from django.conf.urls import url

from .views.document_views import MailDocumentLinkView
from .views.document_file_views import (
    MailDocumentFileLinkView, MailDocumentFileAttachmentView
)
from .views.document_version_views import (
    MailDocumentVersionLinkView, MailDocumentVersionAttachmentView
)
from .views.mailing_profile_views import (
    UserMailerBackendSelectionView, UserMailingCreateView,
    UserMailingDeleteView, UserMailingEditView, UserMailerTestView,
    UserMailerListView
)


urlpatterns_document = [
    url(
        regex=r'^documents/(?P<document_id>\d+)/send/link/$',
        name='send_document_link_single',
        view=MailDocumentLinkView.as_view()
    ),
    url(
        regex=r'^documents/multiple/send/link/$',
        name='send_document_link_multiple',
        view=MailDocumentLinkView.as_view()
    )
]

urlpatterns_document_file = [
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/send/attachment/$',
        name='send_document_file_attachment_single',
        view=MailDocumentFileAttachmentView.as_view()
    ),
    url(
        regex=r'^documents/files/multiple/send/attachment/$',
        name='send_document_file_attachment_multiple',
        view=MailDocumentFileAttachmentView.as_view()
    ),
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/send/link/$',
        name='send_document_file_link_single',
        view=MailDocumentFileLinkView.as_view()
    ),
    url(
        regex=r'^documents/files/multiple/send/link/$',
        name='send_document_file_link_multiple',
        view=MailDocumentFileLinkView.as_view()
    )
]

urlpatterns_document_version = [
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/send/attachment/$',
        name='send_document_version_attachment_single',
        view=MailDocumentVersionAttachmentView.as_view()
    ),
    url(
        regex=r'^documents/versions/multiple/send/attachment/$',
        name='send_document_version_attachment_multiple',
        view=MailDocumentVersionAttachmentView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/send/link/$',
        name='send_document_version_link_single',
        view=MailDocumentVersionLinkView.as_view()
    ),
    url(
        regex=r'^documents/versions/multiple/send/link/$',
        name='send_document_version_link_multiple',
        view=MailDocumentVersionLinkView.as_view()
    )
]

urlpatterns_user_mailers = [
    url(
        regex=r'^user_mailers/backend/selection/$',
        name='user_mailer_backend_selection',
        view=UserMailerBackendSelectionView.as_view()
    ),
    url(
        regex=r'^user_mailers/(?P<class_path>[a-zA-Z0-9_.]+)/create/$',
        name='user_mailer_create', view=UserMailingCreateView.as_view()
    ),
    url(
        regex=r'^user_mailers/(?P<mailer_id>\d+)/delete/$',
        name='user_mailer_delete', view=UserMailingDeleteView.as_view()
    ),
    url(
        regex=r'^user_mailers/(?P<mailer_id>\d+)/edit/$',
        name='user_mailer_edit', view=UserMailingEditView.as_view()
    ),
    url(
        regex=r'^user_mailers/(?P<mailer_id>\d+)/test/$',
        name='user_mailer_test', view=UserMailerTestView.as_view()
    ),
    url(
        regex=r'^user_mailers/$', name='user_mailer_list',
        view=UserMailerListView.as_view()
    )
]

urlpatterns = []
urlpatterns.extend(urlpatterns_document)
urlpatterns.extend(urlpatterns_document_file)
urlpatterns.extend(urlpatterns_document_version)
urlpatterns.extend(urlpatterns_user_mailers)
