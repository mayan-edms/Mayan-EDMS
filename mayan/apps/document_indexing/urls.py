from django.conf.urls import url

from .api_views import (
    APIDocumentIndexInstanceNodeListView, APIIndexInstanceDetailView,
    APIIndexInstanceListView, APIIndexInstanceNodeDetailView,
    APIIndexInstanceNodeDocumentListView, APIIndexInstanceNodeListView,
    APIIndexTemplateDetailView, APIIndexTemplateDocumentTypeAddView,
    APIIndexTemplateDocumentTypeListView,
    APIIndexTemplateDocumentTypeRemoveView, APIIndexTemplateListView,
    APIIndexTemplateNodeListView, APIIndexTemplateNodeDetailView,
    APIIndexTemplateRebuildView, APIIndexTemplateResetView
)

from .views.index_instance_views import (
    DocumentIndexInstanceNodeListView, IndexInstanceNodeView,
    IndexInstanceListView
)
from .views.index_template_views import (
    DocumentTypeIndexTemplateListView, IndexTemplateAllRebuildView,
    IndexTemplateCreateView, IndexTemplateDeleteView,
    IndexTemplateDocumentTypesView, IndexTemplateEditView,
    IndexTemplateListView, IndexTemplateNodeListView,
    IndexTemplateNodeCreateView, IndexTemplateNodeDeleteView,
    IndexTemplateNodeEditView, IndexTemplateRebuildView,
    IndexTemplateResetView
)

urlpatterns_templates = [
    url(
        regex=r'^document_types/(?P<document_type_id>\d+)/index_templates/$',
        name='document_type_index_templates',
        view=DocumentTypeIndexTemplateListView.as_view()
    ),
    url(
        regex=r'^templates/$', name='index_template_list',
        view=IndexTemplateListView.as_view()
    ),
    url(
        regex=r'^templates/create/$', name='index_template_create',
        view=IndexTemplateCreateView.as_view()
    ),
    url(
        regex=r'^templates/(?P<index_template_id>\d+)/delete/$',
        name='index_template_delete', view=IndexTemplateDeleteView.as_view()
    ),
    url(
        regex=r'^templates/(?P<index_template_id>\d+)/document_types/$',
        name='index_template_document_types',
        view=IndexTemplateDocumentTypesView.as_view()
    ),
    url(
        regex=r'^templates/(?P<index_template_id>\d+)/edit/$',
        name='index_template_edit', view=IndexTemplateEditView.as_view()
    ),
    url(
        regex=r'^templates/(?P<index_template_id>\d+)/nodes/$',
        name='index_template_view',
        view=IndexTemplateNodeListView.as_view()
    ),
    url(
        regex=r'^templates/(?P<index_template_id>\d+)/rebuild/$',
        name='index_template_rebuild', view=IndexTemplateRebuildView.as_view()
    ),
    url(
        regex=r'^templates/nodes/(?P<index_template_node_id>\d+)/children/create/$',
        name='template_node_create', view=IndexTemplateNodeCreateView.as_view()
    ),
    url(
        regex=r'^templates/nodes/(?P<index_template_node_id>\d+)/delete/$',
        name='template_node_delete', view=IndexTemplateNodeDeleteView.as_view()
    ),
    url(
        regex=r'^templates/nodes/(?P<index_template_node_id>\d+)/edit/$',
        name='template_node_edit', view=IndexTemplateNodeEditView.as_view()
    )
]

urlpatterns_instances = [
    url(
        regex=r'^instances/$', name='index_list', view=IndexInstanceListView.as_view()
    ),
    url(
        regex=r'^instances/nodes/(?P<index_instance_node_id>\d+)/$',
        name='index_instance_node_view', view=IndexInstanceNodeView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/instances/$',
        name='document_index_list', view=DocumentIndexInstanceNodeListView.as_view()
    )
]

urlpatterns_tools = [
    url(
        regex=r'^instances/rebuild/$', name='rebuild_index_instances',
        view=IndexTemplateAllRebuildView.as_view()
    ),
    url(
        regex=r'^instances/reset/$', name='index_instances_reset',
        view=IndexTemplateResetView.as_view()
    )
]

urlpatterns = []
urlpatterns.extend(urlpatterns_templates)
urlpatterns.extend(urlpatterns_instances)
urlpatterns.extend(urlpatterns_tools)

api_urls_document_indexes = [
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/indexes/$',
        name='document-index-list',
        view=APIDocumentIndexInstanceNodeListView.as_view()
    ),
]

api_urls_index_instances = [
    url(
        regex=r'^index_instances/$', name='indexinstance-list',
        view=APIIndexInstanceListView.as_view()
    ),
    url(
        regex=r'^index_instances/(?P<index_instance_id>[0-9]+)/$',
        name='indexinstance-detail', view=APIIndexInstanceDetailView.as_view()
    ),
    url(
        regex=r'^index_instances/(?P<index_instance_id>[0-9]+)/nodes/$',
        name='indexinstancenode-list', view=APIIndexInstanceNodeListView.as_view()
    ),
    url(
        regex=r'^index_instances/(?P<index_instance_id>[0-9]+)/nodes/(?P<index_instance_node_id>[0-9]+)/$',
        name='indexinstancenode-detail',
        view=APIIndexInstanceNodeDetailView.as_view()
    ),
    url(
        regex=r'^index_instances/(?P<index_instance_id>[0-9]+)/nodes/(?P<index_instance_node_id>[0-9]+)/documents/$',
        name='indexinstancenode-document-list',
        view=APIIndexInstanceNodeDocumentListView.as_view()
    ),
]

api_urls_index_templates = [
    url(
        regex=r'^index_templates/$', name='indextemplate-list',
        view=APIIndexTemplateListView.as_view()
    ),
    url(
        regex=r'^index_templates/(?P<index_template_id>[0-9]+)/$',
        name='indextemplate-detail',
        view=APIIndexTemplateDetailView.as_view()
    ),
    url(
        regex=r'^index_templates/(?P<index_template_id>[0-9]+)/document_types/$',
        name='indextemplate-documenttype-list',
        view=APIIndexTemplateDocumentTypeListView.as_view()
    ),
    url(
        regex=r'^index_templates/(?P<index_template_id>[0-9]+)/document_types/add/$',
        name='indextemplate-documenttype-add',
        view=APIIndexTemplateDocumentTypeAddView.as_view()
    ),
    url(
        regex=r'^index_templates/(?P<index_template_id>[0-9]+)/document_types/remove/$',
        name='indextemplate-documenttype-remove',
        view=APIIndexTemplateDocumentTypeRemoveView.as_view()
    ),
    url(
        regex=r'^index_templates/(?P<index_template_id>[0-9]+)/rebuild/$',
        name='indextemplate-rebuild',
        view=APIIndexTemplateRebuildView.as_view()
    ),
    url(
        regex=r'^index_templates/(?P<index_template_id>[0-9]+)/reset/$',
        name='indextemplate-reset',
        view=APIIndexTemplateResetView.as_view()
    ),
    url(
        regex=r'^index_templates/(?P<index_template_id>[0-9]+)/nodes/$',
        name='indextemplatenode-list',
        view=APIIndexTemplateNodeListView.as_view()
    ),
    url(
        regex=r'^index_templates/(?P<index_template_id>[0-9]+)/nodes/(?P<index_template_node_id>[0-9]+)/$',
        name='indextemplatenode-detail', view=APIIndexTemplateNodeDetailView.as_view()
    ),
]

api_urls = []
api_urls.extend(api_urls_document_indexes)
api_urls.extend(api_urls_index_instances)
api_urls.extend(api_urls_index_templates)
