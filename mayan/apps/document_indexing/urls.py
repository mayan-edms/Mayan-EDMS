from django.conf.urls import url

from .api_views import (
    APIDocumentIndexInstanceNodeListView, APIIndexInstanceDetailView,
    APIIndexInstanceListView, APIIndexInstanceNodeDetailView,
    APIIndexInstanceNodeListView, APIIndexInstanceNodeDocumentListView,
    APIIndexTemplateDetailView, APIIndexTemplateListView,
    APIIndexTemplateNodeListView, APIIndexTemplateNodeDetailView
)
from .views import (
    DocumentIndexNodeListView, DocumentTypeIndexesView, IndexInstanceNodeView,
    IndexListView, IndexesRebuildView, IndexesResetView,
    SetupIndexDocumentTypesView, SetupIndexCreateView, SetupIndexDeleteView,
    SetupIndexEditView, SetupIndexListView, SetupIndexRebuildView,
    SetupIndexTreeTemplateListView, TemplateNodeCreateView,
    TemplateNodeDeleteView, TemplateNodeEditView
)

urlpatterns_templates = [
    url(
        regex=r'^document_types/(?P<document_type_id>\d+)/index_templates/$',
        name='document_type_index_templates',
        view=DocumentTypeIndexesView.as_view()
    ),
    url(
        regex=r'^templates/$', name='index_setup_list',
        view=SetupIndexListView.as_view()
    ),
    url(
        regex=r'^templates/create/$', name='index_setup_create',
        view=SetupIndexCreateView.as_view()
    ),
    url(
        regex=r'^templates/(?P<index_template_id>\d+)/delete/$',
        name='index_setup_delete', view=SetupIndexDeleteView.as_view()
    ),
    url(
        regex=r'^templates/(?P<index_template_id>\d+)/document_types/$',
        name='index_setup_document_types',
        view=SetupIndexDocumentTypesView.as_view()
    ),
    url(
        regex=r'^templates/(?P<index_template_id>\d+)/edit/$',
        name='index_setup_edit', view=SetupIndexEditView.as_view()
    ),
    url(
        regex=r'^templates/(?P<index_template_id>\d+)/nodes/$',
        name='index_setup_view',
        view=SetupIndexTreeTemplateListView.as_view()
    ),
    url(
        regex=r'^templates/(?P<index_template_id>\d+)/rebuild/$',
        name='index_setup_rebuild', view=SetupIndexRebuildView.as_view()
    ),
    url(
        regex=r'^templates/nodes/(?P<index_template_node_id>\d+)/children/create/$',
        name='template_node_create', view=TemplateNodeCreateView.as_view()
    ),
    url(
        regex=r'^templates/nodes/(?P<index_template_node_id>\d+)/delete/$',
        name='template_node_delete', view=TemplateNodeDeleteView.as_view()
    ),
    url(
        regex=r'^templates/nodes/(?P<index_template_node_id>\d+)/edit/$',
        name='template_node_edit', view=TemplateNodeEditView.as_view()
    )
]

urlpatterns_instances = [
    url(
        regex=r'^instances/$', name='index_list', view=IndexListView.as_view()
    ),
    url(
        regex=r'^instances/nodes/(?P<index_instance_node_id>\d+)/$',
        name='index_instance_node_view', view=IndexInstanceNodeView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/instances/$',
        name='document_index_list', view=DocumentIndexNodeListView.as_view()
    )
]

urlpatterns_tools = [
    url(
        regex=r'^instances/rebuild/$', name='rebuild_index_instances',
        view=IndexesRebuildView.as_view()
    ),
    url(
        regex=r'^instances/reset/$', name='index_instances_reset',
        view=IndexesResetView.as_view()
    )
]

urlpatterns = []
urlpatterns.extend(urlpatterns_templates)
urlpatterns.extend(urlpatterns_instances)
urlpatterns.extend(urlpatterns_tools)

api_urls = [
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/indexes/$',
        name='document-index-list',
        view=APIDocumentIndexInstanceNodeListView.as_view()
    ),
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
    url(
        regex=r'^index_templates/$', name='indextemplate-list',
        view=APIIndexTemplateListView.as_view()
    ),
    url(
        regex=r'^index_templates/(?P<index_template_id>[0-9]+)/$',
        name='indextemplate-detail', view=APIIndexTemplateDetailView.as_view()
    ),
    url(
        regex=r'^index_templates/(?P<index_template_id>[0-9]+)/nodes/$',
        name='indextemplatenode-list', view=APIIndexTemplateNodeListView.as_view()
    ),
    url(
        regex=r'^index_templates/(?P<index_template_id>[0-9]+)/nodes/(?P<index_template_node_id>[0-9]+)/$',
        name='indextemplatenode-detail', view=APIIndexTemplateNodeDetailView.as_view()
    ),
]
