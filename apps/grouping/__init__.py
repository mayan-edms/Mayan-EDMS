from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links

from documents.literals import PERMISSION_DOCUMENT_VIEW
from documents.models import Document

document_group_link = {'text': _(u'group actions'), 'view': 'document_group_view', 'famfam': 'page_go', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
groups_for_document = {'text': _(u'groups'), 'view': 'groups_for_document', 'args': 'object.pk', 'famfam': 'page_go', 'permissions': [PERMISSION_DOCUMENT_VIEW]}

register_links(Document, [groups_for_document], menu_name='form_header')
