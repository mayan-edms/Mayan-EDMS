from django.conf.urls import url

from .views import (
    MailDocumentLinkView, MailDocumentView, UserMailerBackendSelectionView,
    UserMailingCreateView, UserMailingDeleteView, UserMailingEditView,
    UserMailerTestView, UserMailerListView
)

urlpatterns = [
    url(
        regex=r'^documents/(?P<document_id>\d+)/send/link/$',
        name='send_document_link', view=MailDocumentLinkView.as_view()
    ),
    url(
        regex=r'^documents/multiple/send/link/$',
        name='send_multiple_document_link',
        view=MailDocumentLinkView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/send/attachment/$',
        name='send_document_attachment', view=MailDocumentView.as_view()
    ),
    url(
        regex=r'^documents/multiple/send/attachment/$',
        name='send_multiple_document_attachment',
        view=MailDocumentView.as_view()
    ),
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
