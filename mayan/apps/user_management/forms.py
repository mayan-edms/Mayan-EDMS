from django import forms
from django.contrib.auth import get_user_model


class UserForm(forms.ModelForm):
    """
    Form used to edit a user's mininal fields by the user himself
    """
    class Meta:
        fields = (
            'username', 'first_name', 'last_name', 'email', 'is_active',
        )
        model = get_user_model()
