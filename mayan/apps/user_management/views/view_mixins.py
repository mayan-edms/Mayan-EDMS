from django.http import Http404

from mayan.apps.acls.models import AccessControlList

from ..literals import FIELDS_ALL, FIELDS_USER


class DynamicUserViewMixin:
    def dispatch(self, request, *args, **kwargs):
        object_raw = self.get_object(queryset=self.get_source_queryset())
        self.is_current_user = object_raw == self.request.user

        queryset = AccessControlList.objects.restrict_queryset(
            permission=self.object_permission,
            queryset=self.get_source_queryset(),
            user=self.request.user
        )

        try:
            filtered_obj = self.get_object(queryset=queryset)
        except Http404:
            filtered_obj = None

        self.user_has_access = filtered_obj == self.request.user

        return super().dispatch(request=request, *args, **kwargs)

    def get_object_permission(self):
        if self.is_current_user:
            return
        else:
            return self.object_permission


class DynamicUserFormFieldViewMixin(DynamicUserViewMixin):
    def get_form_class(self):
        if self.is_current_user:
            if self.user_has_access:
                self.fields = FIELDS_ALL
            else:
                self.fields = FIELDS_USER
        else:
            self.fields = FIELDS_ALL

        return super().get_form_class()


class DynamicExternalUserViewMixin:
    def dispatch(self, request, *args, **kwargs):
        external_object_raw = self.get_external_object(
            queryset=self.get_external_object_queryset()
        )
        self.is_current_user = external_object_raw == self.request.user

        queryset = AccessControlList.objects.restrict_queryset(
            permission=self.external_object_permission,
            queryset=self.get_external_object_queryset(),
            user=self.request.user
        )

        try:
            external_object_filtered = self.get_external_object(
                queryset=queryset
            )
        except Http404:
            external_object_filtered = None

        self.user_has_access = external_object_filtered == self.request.user

        return super().dispatch(request=request, *args, **kwargs)

    def get_external_object_permission(self):
        if self.is_current_user:
            return
        else:
            return self.external_object_permission
