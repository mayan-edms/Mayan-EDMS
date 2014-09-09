from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _


def has_usable_password(context):
    return context['request'].user.has_usable_password


link_password_change = {'text': _(u'change password'), 'view': 'common:password_change_view', 'famfam': 'computer_key', 'condition': has_usable_password}
link_current_user_details = {'text': _(u'user details'), 'view': 'common:current_user_details', 'famfam': 'vcard'}
link_current_user_edit = {'text': _(u'edit details'), 'view': 'common:current_user_edit', 'famfam': 'vcard_edit'}

link_about = {'text': _(u'about'), 'view': 'common:about_view', 'famfam': 'information'}
link_license = {'text': _(u'license'), 'view': 'common:license_view', 'famfam': 'script'}
