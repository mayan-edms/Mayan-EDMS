from __future__ import unicode_literals

from django.conf.urls import url

from .views import DocumentTemplateSandboxView

urlpatterns = [
    url(
        regex=r'^documents/(?P<pk>\d+)/sandbox/$',
        view=DocumentTemplateSandboxView.as_view(),
        name='document_template_sandbox'
    ),
]
