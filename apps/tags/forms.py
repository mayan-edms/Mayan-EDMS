from __future__ import absolute_import

import logging

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied

from taggit.models import Tag

from acls.models import AccessEntry
from permissions.models import Permission

from .models import COLOR_CHOICES
from .permissions import PERMISSION_TAG_VIEW

logger = logging.getLogger(__name__)


class TagForm(forms.Form):
    """
    Form to edit an existing tag's properties
    """
    name = forms.CharField(label=_(u'Name'))
    color = forms.ChoiceField(choices=COLOR_CHOICES, label=_(u'Color'))


class TagListForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        logger.debug('user: %s' % user)
        super(TagListForm, self).__init__(*args, **kwargs)

        queryset = Tag.objects.all()
        try:
            Permission.objects.check_permissions(user, [PERMISSION_TAG_VIEW])
        except PermissionDenied:
            queryset = AccessEntry.objects.filter_objects_by_access(PERMISSION_TAG_VIEW, user, queryset)

        self.fields['tag'] = forms.ModelChoiceField(
            queryset=queryset,
            label=_(u'Tags'))
