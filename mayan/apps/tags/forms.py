from __future__ import absolute_import, unicode_literals

import logging

from django import forms
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessControlList
from permissions import Permission

from .models import Tag
from .permissions import permission_tag_view

logger = logging.getLogger(__name__)


class TagListForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        logger.debug('user: %s', user)
        super(TagListForm, self).__init__(*args, **kwargs)

        queryset = Tag.on_organization.all()
        try:
            Permission.check_permissions(user, (permission_tag_view,))
        except PermissionDenied:
            queryset = AccessControlList.objects.filter_by_access(
                permission_tag_view, user, queryset
            )

        self.fields['tag'] = forms.ModelChoiceField(
            queryset=queryset,
            label=_('Tags'))


class TagMultipleSelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        logger.debug('user: %s', user)
        super(TagMultipleSelectionForm, self).__init__(*args, **kwargs)

        queryset = Tag.on_organization.all()
        try:
            Permission.check_permissions(user, (permission_tag_view,))
        except PermissionDenied:
            queryset = AccessControlList.objects.filter_by_access(
                permission_tag_view, user, queryset
            )

        self.fields['tags'] = forms.MultipleChoiceField(
            label=_('Tags'), choices=queryset.values_list('id', 'label'),
            help_text=_('Tags to attach to the document.'), required=False,
            widget=forms.CheckboxSelectMultiple
        )
