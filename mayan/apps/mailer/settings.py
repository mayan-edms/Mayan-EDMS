from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_settings

register_settings(
    namespace='mailer',
    module='mailer.settings',
    settings=[
        {'name': 'LINK_SUBJECT_TEMPLATE', 'global_name': 'MAILER_LINK_SUBJECT_TEMPLATE', 'default': _('Link for document: {{ document }}'), 'description': _('Template for the document link email form subject line.')},
        {'name': 'LINK_BODY_TEMPLATE', 'global_name': 'MAILER_LINK_BODY_TEMPLATE', 'default': _('To access this document click on the following link: <a href="{{ link }}">{{ link }}</a><br /><br />\n\n--------<br />\nThis email has been sent from Mayan EDMS (http://www.mayan-edms.com)'), 'description': _('Template for the document link email form body line.')},
        {'name': 'DOCUMENT_SUBJECT_TEMPLATE', 'global_name': 'MAILER_DOCUMENT_SUBJECT_TEMPLATE', 'default': _('Document: {{ document }}'), 'description': _('Template for the document email form subject line.')},
        {'name': 'DOCUMENT_BODY_TEMPLATE', 'global_name': 'MAILER_DOCUMENT_BODY_TEMPLATE', 'default': _('Attached to this email is the document: {{ document }}<br /><br />\n\n--------<br />\nThis email has been sent from Mayan EDMS (http://www.mayan-edms.com)'), 'description': _('Template for the document email form body line.')},
    ]
)
