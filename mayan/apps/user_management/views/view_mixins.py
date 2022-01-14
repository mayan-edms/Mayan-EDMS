from django.http import Http404

from mayan.apps.acls.models import AccessControlList

from ..literals import FIELDS_ALL, FIELDS_USER


class DynamicUserViewMixin:
    def dispatch(self, request, *args, **kwargs):
        self.object_raw = self.get_object(queryset=self.get_source_queryset())
        return super().dispatch(request=request, *args, **kwargs)

    def get_form_class(self):
        if self.object_raw == self.request.user:
            # Is current user.

            queryset = AccessControlList.objects.restrict_queryset(
                permission=self.object_permission,
                queryset=self.get_source_queryset(),
                user=self.request.user
            )

            try:
                filtered_obj = self.get_object(queryset=queryset)
            except Http404:
                filtered_obj = None

            if filtered_obj == self.request.user:
                # Current user has necessary object access granted.
                self.fields = FIELDS_ALL
            else:
                self.fields = FIELDS_USER
        else:
            self.fields = FIELDS_ALL

        return super().get_form_class()

    def get_object_permission(self):
        if self.object_raw == self.request.user:
            return
        else:
            return self.object_permission
