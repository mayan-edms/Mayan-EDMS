from __future__ import unicode_literals

from django.contrib import admin

from .models import Key


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    #date_hierarchy = 'datetime'
    list_display = ('key_id', 'user_id', 'key_type')
    #readonly_fields = list_display

    """
    key_id = models.CharField(
        max_length=16, unique=True, verbose_name=_('Key ID')
    )
    creation_date = models.DateField(verbose_name=_('Creation date'))
    expiration_date = models.DateField(verbose_name=_('Expiration date'))
    fingerprint = models.CharField(
        max_length=40, verbose_name=_('Fingerprint')
    )
    length = models.PositiveIntegerField(verbose_name=_('Length'))
    algorithm = models.PositiveIntegerField(verbose_name=_('Algorithm'))
    user_id = models.TextField(verbose_name=_('User ID'))
    key_type = models.CharField(max_length=3, verbose_name=_('Type'))
    """
