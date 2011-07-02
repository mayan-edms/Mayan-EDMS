from django.utils.translation import ugettext_lazy as _

from documents.literals import PERMISSION_DOCUMENT_VIEW

document_group_link = {'text': _(u'group actions'), 'view': 'document_group_view', 'famfam': 'page_go', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
