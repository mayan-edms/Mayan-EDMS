from __future__ import absolute_import

from django import forms

from .models import BackupJob


class BackupJobForm(forms.ModelForm):
    #expiration_datetime = SplitTimeDeltaField()

    class Meta:
        model = BackupJob
        #exclude = ('checkout_datetime', 'user_content_type', 'user_object_id')

        #widgets = {
        #    'document': forms.widgets.HiddenInput(),
        #}

    #def clean_document(self):
    #    document = self.cleaned_data['document']
    #    if document.is_checked_out():
    #        raise DocumentAlreadyCheckedOut
    #    return document
