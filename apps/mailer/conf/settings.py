"""Configuration options for the mailer app"""

from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_settings

register_settings(
    namespace=u'mailer',
    module=u'mailer.conf.settings',
    settings=[
        # Links
        {'name': u'LINK_SUBJECT_TEMPLATE', 'global_name': u'MAILER_LINK_SUBJECT_TEMPLATE', 'default': 'Link for document: {{ document }}', 'description': _(u'Template for the document link email form subject line.')},
        {'name': u'LINK_BODY_TEMPLATE', 'global_name': u'MAILER_LINK_BODY_TEMPLATE', 'default': 'To access this document click on the following link: <a href="{{ link }}">{{ link }}</a><br /><br />\n\n--------<br />\nThis email has been sent from Mayan EDMS (http://www.mayan-edms.com)', 'description': _(u'Template for the document link email form body line.')},
        # Attachment
        {'name': u'DOCUMENT_SUBJECT_TEMPLATE', 'global_name': u'MAILER_DOCUMENT_SUBJECT_TEMPLATE', 'default': 'Document: {{ document }}', 'description': _(u'Template for the document email form subject line.')},
        {'name': u'DOCUMENT_BODY_TEMPLATE', 'global_name': u'MAILER_DOCUMENT_BODY_TEMPLATE', 'default': 'Attached to this email is the document: {{ document }}<br /><br />\n\n--------<br />\nThis email has been sent from Mayan EDMS (http://www.mayan-edms.com)', 'description': _(u'Template for the document email form body line.')},
    ]
)
