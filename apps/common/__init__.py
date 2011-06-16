import tempfile

from django.utils.translation import ugettext_lazy as _

from common.conf import settings as common_settings
from navigation.api import register_links

TEMPORARY_DIRECTORY = common_settings.TEMPORARY_DIRECTORY \
    if common_settings.TEMPORARY_DIRECTORY else tempfile.mkdtemp()


def has_usable_password(context):
    return context['request'].user.has_usable_password

password_change_view = {'text': _(u'change password'), 'view': 'password_change_view', 'famfam': 'computer_key', 'condition': has_usable_password}
current_user_details = {'text': _(u'user details'), 'view': 'current_user_details', 'famfam': 'vcard'}
current_user_edit = {'text': _(u'edit details'), 'view': 'current_user_edit', 'famfam': 'vcard_edit'}

register_links(['current_user_details', 'current_user_edit', 'password_change_view'], [current_user_details, current_user_edit, password_change_view], menu_name='secondary_menu')
