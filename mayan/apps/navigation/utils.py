from __future__ import absolute_import, unicode_literals

from django.apps import apps
from django.core.exceptions import PermissionDenied

from permissions import Permission


def get_cascade_condition(app_label, model_name, object_permission, view_permission=None):
    """
    Return a function that first checks to see if the user has the view
    permission. If not, then filters the objects with the object permission
    and return True if there is at least one item in the filtered queryset.
    This is used to avoid showing a link that ends up in a view with an
    empty results set.
    """
    def condition(context):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        Model = apps.get_model(app_label=app_label, model_name=model_name)

        if view_permission:
            try:
                Permission.check_permissions(
                    requester=context.request.user,
                    permissions=(view_permission,)
                )
            except PermissionDenied:
                pass
            else:
                return True

        queryset = AccessControlList.objects.filter_by_access(
            permission=object_permission, user=context.request.user,
            queryset=Model.objects.all()
        )
        return queryset.count() > 0

    return condition
