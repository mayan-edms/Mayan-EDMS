from django.utils.translation import ugettext as _

from tags import tag_document_remove


def get_tags_subtemplate(obj):
    """
    Return all the settings to render a subtemplate containing and
    object's tags
    """
    return {
        'name': 'generic_list_subtemplate.html',
        'title': _(u'tags'),
        'object_list': obj.tags.all(),
        'hide_link': True,
        'navigation_object_links': [tag_document_remove],
    }
