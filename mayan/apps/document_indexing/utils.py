from django.utils.translation import ugettext_lazy as _

from document_indexing.api import get_breadcrumbs


def get_document_indexing_subtemplate(document):
    """
    Return all the settings to render a subtemplate containing a
    list of index instances where a document may be found
    """
    object_list = []

    for index_instance in document.indexinstance_set.all():
        object_list.append(get_breadcrumbs(index_instance, single_link=True, include_count=True))

    return {
            'name': 'generic_list_subtemplate.html',
            'context': {
                'title': _(u'document indexes'),
                'object_list': object_list,
                'hide_link': True
            }
        }
