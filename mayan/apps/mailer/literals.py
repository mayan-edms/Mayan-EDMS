from django.utils.translation import ugettext_lazy as _


DEFAULT_DOCUMENT_BODY_TEMPLATE = _(
    'Attached to this email is the document: {{ document }}\n\n '
    '--------\n '
    'This email has been sent from %(project_title)s (%(project_website)s)'
)
DEFAULT_DOCUMENT_SUBJECT_TEMPLATE = _('Document: {{ document }}')
DEFAULT_LINK_BODY_TEMPLATE = _(
    'To access this document click on the following link: '
    '{{ link }}\n\n--------\n '
    'This email has been sent from %(project_title)s (%(project_website)s)'
)
DEFAULT_LINK_SUBJECT_TEMPLATE = _('Link for document: {{ document }}')
EMAIL_SEPARATORS = (',', ';')
