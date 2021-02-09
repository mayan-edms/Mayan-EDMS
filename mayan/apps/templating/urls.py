from django.conf.urls import url

from .api_views import APITemplateDetailView, APITemplateListView

from .views import DocumentTemplateSandboxView

urlpatterns = [
    url(
        regex=r'^documents/(?P<document_id>\d+)/sandbox/$',
        name='document_template_sandbox',
        view=DocumentTemplateSandboxView.as_view()
    ),
]

api_urls = [
    url(
        regex=r'^templates/$', view=APITemplateListView.as_view(),
        name='template-list'
    ),
    url(
        regex=r'^templates/(?P<name>[-\w]+)/$',
        view=APITemplateDetailView.as_view(), name='template-detail'
    )
]
