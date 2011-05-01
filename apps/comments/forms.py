from django import forms
from django.contrib.comments.models import Comment


class CommentForm(forms.ModelForm):
    """
    A standard model form to allow users to post a comment
    """
    class Meta:
        model = Comment
        fields = ('comment',)
