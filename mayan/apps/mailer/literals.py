from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _


DEFAULT_DOCUMENT_BODY_TEMPLATE = _(
    'Attached to this email is the document: {{ document }}<br /><br />\n\n\
    --------<br />\nThis email has been sent from \
     %(project_title)s (%(project_website)s)'
) % {
    'project_title': settings.PROJECT_TITLE,
    'project_website': settings.PROJECT_WEBSITE
}

DEFAULT_LINK_BODY_TEMPLATE = _(
    'To access this document click on the following link: \
    <a href="{{ link }}">{{ link }}</a><br /><br />\n\n--------<br />\
    \nThis email has been sent from %(project_title)s (%(project_website)s)'
) % {
    'project_title': settings.PROJECT_TITLE,
    'project_website': settings.PROJECT_WEBSITE
}
