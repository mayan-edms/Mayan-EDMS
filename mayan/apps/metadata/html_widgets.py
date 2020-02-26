from __future__ import absolute_import, unicode_literals

from django.apps import apps
from django.template.loader import render_to_string

from .permissions import permission_metadata_view


def widget_document_metadata(context):
    """
    A widget that displays the metadata for the given document
    """
    AccessControlList = apps.get_model(
        app_label='acls', model_name='AccessControlList'
    )
    queryset = AccessControlList.objects.restrict_queryset(
        queryset=context['object'].metadata.all(),
        permission=permission_metadata_view,
        user=context['user']
    )

    return render_to_string(
        template_name='metadata/document_metadata_widget.html', context={
            'queryset': queryset
        }
    )
