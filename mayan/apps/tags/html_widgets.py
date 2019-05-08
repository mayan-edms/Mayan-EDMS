from __future__ import absolute_import, unicode_literals

from django.template.loader import render_to_string

from .permissions import permission_tag_view


def widget_document_tags(document, user):
    """
    A tag widget that displays the tags for the given document
    """
    return render_to_string(
        template_name='tags/document_tags_widget.html', context={
            'tags': document.get_tags(
                permission=permission_tag_view, user=user
            )
        }
    )


def widget_single_tag(tag):
    return render_to_string(
        template_name='tags/tag_widget.html', context={'tag': tag}
    )
