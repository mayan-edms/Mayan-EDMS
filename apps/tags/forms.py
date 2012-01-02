from __future__ import absolute_import

from django import forms
from django.utils.translation import ugettext_lazy as _

from taggit.models import Tag

from .models import COLOR_CHOICES


class AddTagForm(forms.Form):
    """
    Form to be displayed in the sidebar of a document and allow adding
    new or existing tags
    """
    new_tag = forms.CharField(required=False, label=_(u'New tag'))
    color = forms.ChoiceField(choices=COLOR_CHOICES, required=False, label=_(u'Color'))
    existing_tags = forms.ModelChoiceField(required=False, queryset=Tag.objects.all(), label=_(u'Existing tags'))


class TagForm(forms.Form):
    """
    Form to edit an existing tag's properties
    """
    name = forms.CharField(label=_(u'Name'))
    color = forms.ChoiceField(choices=COLOR_CHOICES, label=_(u'Color'))
