from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('label',)
    search_fields = ('label',)


class OrganizationAdminMixin(object):
    def __init__(self, *args, **kwargs):
        super(OrganizationAdminMixin, self).__init__(*args, **kwargs)
        self.list_display = ('organization',) + self.list_display
        self.list_filter = self.list_filter + ('organization',)
        self.ordering = self.ordering or ()
        self.ordering = ('organization',) + self.ordering

    def get_fieldsets(self, *args, **kwargs):
        result = super(OrganizationAdminMixin, self).get_fieldsets(*args, **kwargs)

        if 'organization' in result[0][1]['fields']:
            try:
                result[0][1]['fields'] = result[0][1]['fields'] - ('organization',)
            except TypeError:
                result[0][1]['fields'].remove('organization')

        result = ((_('Organizations'), {
            'fields': ('organization',),
        },),) + tuple(result)

        return result
