from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

FIXTURE_TYPE_JSON = 'json'
FIXTURE_TYPE_YAML = 'yaml'
FIXTURE_TYPE_XML = 'xml'

FIXTURE_TYPES_CHOICES = (
    (FIXTURE_TYPE_JSON, _(u'JSON')),
    (FIXTURE_TYPE_YAML, _(u'YAML')),
    (FIXTURE_TYPE_XML, _(u'XML')),
)

FIXTURE_FILE_TYPE = {
    FIXTURE_TYPE_JSON: 'json',
    FIXTURE_TYPE_YAML: 'yaml',
    FIXTURE_TYPE_XML: 'xml',
}

