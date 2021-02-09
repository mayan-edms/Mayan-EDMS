from django import forms
from django.core.exceptions import ImproperlyConfigured

from mayan.apps.acls.models import AccessControlList


class FilteredModelFieldMixin:
    def __init__(self, *args, **kwargs):
        self.source_model = kwargs.pop('source_model', None)
        self.permission = kwargs.pop('permission', None)
        self.source_queryset = kwargs.pop('source_queryset', None)

        if self.source_queryset is None:
            if self.source_model:
                self.source_queryset = self.source_model._meta.default_manager.all()
            else:
                raise ImproperlyConfigured(
                    '{} requires a source_queryset or a source_model to be '
                    'specified as keyword argument.'.format(
                        self.__class__.__name__
                    )
                )

        kwargs['queryset'] = self.source_queryset.none()

        super().__init__(*args, **kwargs)

    def reload(self):
        if self.permission and self.user:
            self.queryset = AccessControlList.objects.restrict_queryset(
                permission=self.permission, queryset=self.source_queryset,
                user=self.user
            )
        else:
            self.queryset = self.source_queryset


class FilteredModelChoiceField(
    FilteredModelFieldMixin, forms.ModelChoiceField
):
    """Single selection filtered model choice field"""


class FilteredModelMultipleChoiceField(
    FilteredModelFieldMixin, forms.ModelMultipleChoiceField
):
    """Multiple selection filtered model choice field"""
