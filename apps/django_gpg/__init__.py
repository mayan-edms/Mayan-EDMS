from django.utils.translation import ugettext_lazy as _

from documents.models import Document
from navigation.api import register_links, register_top_menu, \
    register_model_list_columns, register_multi_item_links, \
    register_sidebar_template
from main.api import register_diagnostic, register_maintenance_links
from permissions.api import register_permission, set_namespace_title
from project_setup.api import register_setup

PERMISSION_DOCUMENT_VERIFY = {'namespace': 'django_gpg', 'name': 'document_verify', 'label': _(u'Verify document signatures')}

# Permission setup
set_namespace_title('django_gpg', _(u'Signatures'))
register_permission(PERMISSION_DOCUMENT_VERIFY)

document_verify = {'text': _(u'Signatures'), 'view': 'document_verify', 'args': 'object.pk', 'famfam': 'text_signature', 'permissions': [PERMISSION_DOCUMENT_VERIFY]}

register_links(Document, [document_verify], menu_name='form_header')
