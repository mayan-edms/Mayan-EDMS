from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _


def method_get_metadata(self, internal_name):
    return self.metadata.get(metadata_type__name=internal_name)


method_get_metadata.short_description = _(
    'get_metadata(< metadata type internal name >)'
)
method_get_metadata.help_text = _(
    'Return the specified document metadata entry.'
)
