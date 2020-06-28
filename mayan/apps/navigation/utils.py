import logging

from django.apps import apps
from django.core.exceptions import PermissionDenied
from django.template import Variable, VariableDoesNotExist
from django.urls import Resolver404, resolve

from mayan.apps.permissions import Permission

logger = logging.getLogger(name=__name__)


def get_cascade_condition(
    app_label, model_name, object_permission, view_permission=None
):
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

        try:
            request = context.request
        except AttributeError:
            # Simple request extraction failed. Might not be a view context.
            # Try alternate method.
            try:
                request = Variable('request').resolve(context)
            except VariableDoesNotExist:
                # There is no request variable, most probable a 500 in a test
                # view. Don't return any resolved links then.
                logger.warning('No request variable, aborting cascade resolution')
                return ()

        if view_permission:
            try:
                Permission.check_user_permissions(
                    permissions=(view_permission,), user=request.user
                )
            except PermissionDenied:
                pass
            else:
                return True

        queryset = AccessControlList.objects.restrict_queryset(
            permission=object_permission, user=request.user,
            queryset=Model.objects.all()
        )
        return queryset.count() > 0

    return condition


def get_content_type_kwargs_factory(
    variable_name='resolved_object', result_map=None
):
    if not result_map:
        result_map = {
            'app_label': 'app_label',
            'model_name': 'model_name',
            'object_id': 'object_id'
        }

    def get_kwargs(context):
        ContentType = apps.get_model(
            app_label='contenttypes', model_name='ContentType'
        )

        content_type = ContentType.objects.get_for_model(
            context[variable_name]
        )
        return {
            result_map['app_label']: '"{}"'.format(content_type.app_label),
            result_map['model_name']: '"{}"'.format(content_type.model),
            result_map['object_id']: '{}.pk'.format(variable_name)
        }

    return get_kwargs


def get_current_view_name(request):
    current_path = request.META['PATH_INFO']

    # Get sources: view name, view objects
    try:
        current_view_name = resolve(current_path).view_name
    except Resolver404:
        # Can't figure out which view corresponds to this URL.
        # Most likely it is an invalid URL.
        logger.warning(
            'Can\'t figure out which view corresponds to this '
            'URL: %s; aborting menu resolution.', current_path
        )
    else:
        return current_view_name
