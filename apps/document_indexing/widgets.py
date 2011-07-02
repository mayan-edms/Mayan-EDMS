from django.utils.safestring import mark_safe

from document_indexing.models import IndexInstance


def index_instance_item_link(index_instance_item):
    icon = u'folder_page' if isinstance(index_instance_item, IndexInstance) else u'page'
    return mark_safe(u'<span class="famfam active famfam-%(icon)s"></span><a href="%(url)s">%(text)s</a>' % {
        'url': index_instance_item.get_absolute_url(), 'icon': icon, 'text': index_instance_item})
