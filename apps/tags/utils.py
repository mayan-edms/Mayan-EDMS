from django.utils.translation import ugettext as _

from tags import tag_document_remove


def get_tags_subtemplate(obj):    
    return {
        'name': 'generic_list_subtemplate.html',
        'title': _(u'tags'),
        'object_list': obj.tags.all(),
        'extra_columns': [
            {'name': _(u'color'), 'attribute': lambda x: u'<div style="width: 20px; height: 20px; border: 1px solid black; background: %s;"></div>' % x.tagproperties_set.get().get_color_code()},
        ],
        'hide_link': True,
        'navigation_object_links': {None: {
            'document_view_simple' : {'links': [tag_document_remove]},
            'document_view' : {'links': [tag_document_remove]}
        }}
    }
