from __future__ import absolute_import, unicode_literals

import logging

from django import forms
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessControlList
from permissions import Permission

from .models import Folder
from .permissions import permission_folder_view

logger = logging.getLogger(__name__)


class FolderListForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        logger.debug('user: %s', user)
        super(FolderListForm, self).__init__(*args, **kwargs)

        queryset = Folder.on_organization.all()
        try:
            Permission.check_permissions(user, (permission_folder_view,))
        except PermissionDenied:
            queryset = AccessControlList.objects.filter_by_access(
                permission_folder_view, user, queryset
            )

        self.fields['folder'] = forms.ModelChoiceField(
            queryset=queryset,
            label=_('Folder')
        )
