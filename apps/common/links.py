from django.utils.translation import ugettext_lazy as _

from navigation.api import Link


def has_usable_password(context):
    return context['request'].user.has_usable_password


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


password_change_view = Link(text=_(u'change password'), view='password_change_view', sprite='computer_key', condition=has_usable_password)
current_user_details = Link(text=_(u'user details'), view='current_user_details', sprite='vcard')
current_user_edit = Link(text=_(u'edit details'), view='current_user_edit', sprite='vcard_edit')
about_view = Link(text=_('about'), view='about_view', sprite='information')
license_view = Link(text=_('license'), view='license_view', sprite='script')
sentry = Link(text=_(u'sentry'), view='sentry', sprite='bug', icon='bug.png', condition=is_superuser)
admin_site = Link(text=_(u'admin site'), view='admin:index', sprite='keyboard', icon='keyboard.png', condition=is_superuser)
