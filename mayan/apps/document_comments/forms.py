from __future__ import unicode_literals

from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """
    A standard model form to allow users to post a comment
    """
    class Meta:
        fields = ('comment',)
        model = Comment
