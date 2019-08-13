from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    SystemMailerLogEntryListView, MailDocumentLinkView, MailDocumentView,
    UserMailerBackendSelectionView, UserMailingCreateView,
    UserMailingDeleteView, UserMailingEditView, UserMailerLogEntryListView,
    UserMailerTestView, UserMailerListView
)

urlpatterns = [
    url(
        regex=r'^documents/(?P<pk>\d+)/send/link/$', view=MailDocumentLinkView.as_view(),
        name='send_document_link'
    ),
    url(
        regex=r'^documents/multiple/send/link/$', view=MailDocumentLinkView.as_view(),
        name='send_multiple_document_link'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/send/document/$', view=MailDocumentView.as_view(),
        name='send_document'
    ),
    url(
        regex=r'^documents/multiple/send/document/$', view=MailDocumentView.as_view(),
        name='send_multiple_document'
    ),
    url(
        regex=r'^system_mailer/log/$', view=SystemMailerLogEntryListView.as_view(),
        name='system_mailer_error_log'
    ),
    url(
        regex=r'^user_mailers/backend/selection/$',
        view=UserMailerBackendSelectionView.as_view(),
        name='user_mailer_backend_selection'
    ),
    url(
        regex=r'^user_mailers/(?P<class_path>[a-zA-Z0-9_.]+)/create/$',
        view=UserMailingCreateView.as_view(), name='user_mailer_create'
    ),
    url(
        regex=r'^user_mailers/(?P<pk>\d+)/delete/$',
        view=UserMailingDeleteView.as_view(), name='user_mailer_delete'
    ),
    url(
        regex=r'^user_mailers/(?P<pk>\d+)/edit/$',
        view=UserMailingEditView.as_view(), name='user_mailer_edit'
    ),
    url(
        regex=r'^user_mailers/(?P<pk>\d+)/log/$',
        view=UserMailerLogEntryListView.as_view(), name='user_mailer_log'
    ),
    url(
        regex=r'^user_mailers/(?P<pk>\d+)/test/$',
        view=UserMailerTestView.as_view(), name='user_mailer_test'
    ),
    url(
        regex=r'^user_mailers/$', view=UserMailerListView.as_view(),
        name='user_mailer_list'
    ),
]
