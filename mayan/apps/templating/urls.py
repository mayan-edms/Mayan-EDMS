from django.conf.urls import url

from .views import DocumentTemplateSandboxView

urlpatterns = [
    url(
        regex=r'^documents/(?P<document_id>\d+)/sandbox/$',
        name='document_template_sandbox',
        view=DocumentTemplateSandboxView.as_view()
    ),
]
