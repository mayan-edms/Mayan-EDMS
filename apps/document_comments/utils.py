from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.contrib.comments.models import Comment
from . import comment_delete


def get_comments_subtemplate(obj):
    """
    Return all the settings to render a subtemplate containing an
    object's comments
    """
    return {
        'name': 'generic_list_subtemplate.html',
        'context': {
            'title': _(u'comments'),
            'object_list': Comment.objects.for_model(obj).order_by('-submit_date'),
            'hide_link': True,
            'hide_object': True,
            'navigation_object_links': [comment_delete],
            'scrollable_content': True,
            'scrollable_content_height': '200px',
        }
    }
