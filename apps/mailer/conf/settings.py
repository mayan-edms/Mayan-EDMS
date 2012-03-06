"""Configuration options for the mailer app"""

from django.utils.translation import ugettext_lazy as _

from smart_settings.api import Setting, SettingNamespace

mailer_namespace = SettingNamespace('mailer', _(u'Mailer'), module='mailer.conf.settings')

Setting(
    namespace=mailer_namespace,
    name='LINK_SUBJECT_TEMPLATE',
    global_name='MAILER_LINK_SUBJECT_TEMPLATE',
    default=_(u'Link for document: {{ document }}'),
    description=_(u'Template for the document link email form subject line.')
)

Setting(
    namespace=mailer_namespace,
    name='LINK_BODY_TEMPLATE',
    global_name='MAILER_LINK_BODY_TEMPLATE',
    default=_(u'To access this document click on the following link: <a href="{{ link }}">{{ link }}</a><br /><br />\n\n--------<br />\nThis email has been sent from Mayan EDMS (http://www.mayan-edms.com)'),
    description=_(u'Template for the document link email form body line.')
)

Setting(
    namespace=mailer_namespace,
    name='DOCUMENT_SUBJECT_TEMPLATE',
    global_name='MAILER_DOCUMENT_SUBJECT_TEMPLATE',
    default=_(u'Document: {{ document }}'),
    description=_(u'Template for the document email form subject line.')
)

Setting(
    namespace=mailer_namespace,
    name='DOCUMENT_BODY_TEMPLATE',
    global_name='MAILER_DOCUMENT_BODY_TEMPLATE',
    default=_(u'Attached to this email is the document: {{ document }}<br /><br />\n\n--------<br />\nThis email has been sent from Mayan EDMS (http://www.mayan-edms.com)'),
    description=_(u'Template for the document email form body line.')
)
