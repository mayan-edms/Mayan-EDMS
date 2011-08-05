from django.utils.safestring import mark_safe

from document_indexing.models import IndexInstance

FOLDER_W_DOCUMENTS = u'folder_page'
FOLDER_ICON = u'folder'


def index_instance_item_link(index_instance_item):
    if isinstance(index_instance_item, IndexInstance):
        if index_instance_item.index.link_documents:
            icon = FOLDER_W_DOCUMENTS
        else:
            icon = FOLDER_ICON
    else:
        icon = u''
    icon_template = u'<span class="famfam active famfam-%s"></span>' % icon if icon else u''
    return mark_safe('%(icon_template)s<a href="%(url)s">%(text)s</a>' % {
        'url': index_instance_item.get_absolute_url(),
        'icon_template': icon_template,
        'text': index_instance_item
    })
