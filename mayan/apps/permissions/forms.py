from mayan.apps.views.forms import DetailForm

from .models import StoredPermission


class StoredPermissionDetailForm(DetailForm):
    class Meta:
        fields = ('namespace', 'name')
        model = StoredPermission
