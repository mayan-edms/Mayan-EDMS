from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_DOCUMENT_BODY_TEMPLATE, DEFAULT_DOCUMENT_SUBJECT_TEMPLATE,
    DEFAULT_LINK_BODY_TEMPLATE, DEFAULT_LINK_SUBJECT_TEMPLATE
)

namespace = SettingNamespace(label=_('Mailing'), name='mailer')

setting_document_subject_template = namespace.add_setting(
    default=DEFAULT_DOCUMENT_SUBJECT_TEMPLATE,
    global_name='MAILER_DOCUMENT_SUBJECT_TEMPLATE', help_text=_(
        'Template for the document email form subject line.'
    )
)
setting_document_body_template = namespace.add_setting(
    default=DEFAULT_DOCUMENT_BODY_TEMPLATE,
    global_name='MAILER_DOCUMENT_BODY_TEMPLATE', help_text=_(
        'Template for the document email form body text. Can include HTML.'
    )
)
setting_link_subject_template = namespace.add_setting(
    default=DEFAULT_LINK_SUBJECT_TEMPLATE,
    global_name='MAILER_LINK_SUBJECT_TEMPLATE', help_text=_(
        'Template for the document link email form subject line.'
    )
)
setting_link_body_template = namespace.add_setting(
    default=DEFAULT_LINK_BODY_TEMPLATE,
    global_name='MAILER_LINK_BODY_TEMPLATE', help_text=_(
        'Template for the document link email form body text. Can '
        'include HTML.'
    )
)
