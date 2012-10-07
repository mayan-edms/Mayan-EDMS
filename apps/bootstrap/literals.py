from __future__ import absolute_import

import re
try:
    import yaml
except ImportError:
    YAML_AVAILABLE = False
else:
    YAML_AVAILABLE = True

from django.utils.translation import ugettext_lazy as _

FIXTURE_TYPE_JSON = 'json'
FIXTURE_TYPE_YAML = 'yaml'
FIXTURE_TYPE_BETTER_YAML = 'better_yaml'
FIXTURE_TYPE_XML = 'xml'

FIXTURE_TYPES_CHOICES = (
    (FIXTURE_TYPE_JSON, _(u'JSON')),
    # Disabing XML until a way to specify a null pk is found
    #(FIXTURE_TYPE_XML, _(u'XML')),
)

FIXTURE_FILE_TYPE = {
    FIXTURE_TYPE_JSON: 'json',
    FIXTURE_TYPE_YAML: 'yaml',
    FIXTURE_TYPE_BETTER_YAML: 'better_yaml',
    FIXTURE_TYPE_XML: 'xml',
}

FIXTURE_TYPE_PK_NULLIFIER = {
    FIXTURE_TYPE_JSON: lambda x: re.sub('"pk": [0-9]{1,5}', '"pk": null', x),
    FIXTURE_TYPE_YAML: lambda x: re.sub('pk: [0-9]{1,5}', 'pk: null', x),
    FIXTURE_TYPE_BETTER_YAML: lambda x: re.sub('pk: [0-9]{1,5}', 'pk: null', x),
    FIXTURE_TYPE_XML: lambda x: re.sub('pk="[0-9]{1,5}"', 'pk=null', x),
}

FIXTURE_TYPE_EMPTY_FIXTURE = {
    FIXTURE_TYPE_JSON: lambda x: '[]' in x or x == ',',
    FIXTURE_TYPE_YAML: lambda x: '[]' in x,
    FIXTURE_TYPE_BETTER_YAML: lambda x: '{}' in x,
    FIXTURE_TYPE_XML: lambda x: x,
}

FIXTURE_TYPE_MODEL_PROCESS = {
    FIXTURE_TYPE_JSON: lambda x: '%s,' % x[2:-2],
    FIXTURE_TYPE_YAML: lambda x: x,
    FIXTURE_TYPE_BETTER_YAML: lambda x: x,
    FIXTURE_TYPE_XML: lambda x: x,
}

FIXTURE_TYPE_FIXTURE_PROCESS = {
    FIXTURE_TYPE_JSON: lambda x: '[\n%s\n]' % x,
    FIXTURE_TYPE_YAML: lambda x: x,
    FIXTURE_TYPE_BETTER_YAML: lambda x: x,
    FIXTURE_TYPE_XML: lambda x: x,
}

COMMAND_LOADDATA = 'loaddata'

if YAML_AVAILABLE:
    FIXTURE_TYPES_CHOICES += (FIXTURE_TYPE_YAML, _(u'YAML')),
    FIXTURE_TYPES_CHOICES += (FIXTURE_TYPE_BETTER_YAML, _(u'Better YAML')),
