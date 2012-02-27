from __future__ import absolute_import

import logging

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied

from acls.models import AccessEntry
from permissions.models import Permission

from .models import Folder
from .permissions import PERMISSION_FOLDER_VIEW

logger = logging.getLogger(__name__)


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ('title',)


class FolderListForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        logger.debug('user: %s' % user)
        super(FolderListForm, self).__init__(*args, **kwargs)

        queryset = Folder.objects.all()
        try:
            Permission.objects.check_permissions(user, [PERMISSION_FOLDER_VIEW])
        except PermissionDenied:
            queryset = AccessEntry.objects.filter_objects_by_access(PERMISSION_FOLDER_VIEW, user, queryset)

        self.fields['folder'] = forms.ModelChoiceField(
            queryset=queryset,
            label=_(u'Folder'))
