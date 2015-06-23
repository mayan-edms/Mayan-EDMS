from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from smart_settings import Namespace

namespace = Namespace(name='mailer', label=_('Mailing'))
setting_link_subject_template = namespace.add_setting(global_name='MAILER_LINK_SUBJECT_TEMPLATE', default=_('Link for document: {{ document }}'), help_text=_('Template for the document link email form subject line.'))
setting_link_body_template = namespace.add_setting(global_name='MAILER_LINK_BODY_TEMPLATE', default=_('To access this document click on the following link: <a href="{{ link }}">{{ link }}</a><br /><br />\n\n--------<br />\nThis email has been sent from Mayan EDMS (http://www.mayan-edms.com)'), help_text=_('Template for the document link email form body line.'))
setting_document_subject_template = namespace.add_setting(global_name='MAILER_DOCUMENT_SUBJECT_TEMPLATE', default=_('Document: {{ document }}'), help_text=_('Template for the document email form subject line.'))
setting_document_body_template = namespace.add_setting(global_name='MAILER_DOCUMENT_BODY_TEMPLATE', default=_('Attached to this email is the document: {{ document }}<br /><br />\n\n--------<br />\nThis email has been sent from Mayan EDMS (http://www.mayan-edms.com)'), help_text=_('Template for the document email form body line.'))
