from django.utils.translation import ugettext_lazy as _

from navigation.api import register_sidebar_template

TRANFORMATION_CHOICES = {
    u'rotate': u'-rotate %(degrees)d'
}

formats_list = {'text': _('file formats'), 'view': 'formats_list', 'famfam': 'pictures'}

register_sidebar_template(['formats_list'], 'converter_file_formats_help.html')
