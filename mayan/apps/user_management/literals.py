from django.utils.translation import ugettext_lazy as _

FIELDS_ALL = ('username', 'first_name', 'last_name', 'email', 'is_active')
FIELDS_USER = ('first_name', 'last_name')

FIELDSETS_ALL = (
    (
        _('Account'), {
            'fields': ('username', 'email'),
        }
    ), (
        _('Personal'), {
            'fields': ('first_name', 'last_name')
        },
    ), (
        _('Attributes'), {
            'fields': ('is_active',)
        },
    )
)
FIELDSETS_USER = (
    (
        _('Personal'), {
            'fields': ('first_name', 'last_name')
        },
    ),
)
