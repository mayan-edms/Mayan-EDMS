import logging

from django.utils.deprecation import MiddlewareMixin

from mayan.apps.permissions.classes import Permission
from mayan.apps.user_management.querysets import get_user_queryset

from ..events import (
    event_user_impersonation_ended, event_user_impersonation_started
)
from ..literals import (
    IMPERSONATE_VARIABLE_ID, IMPERSONATE_VARIABLE_DISABLE,
    IMPERSONATE_VARIABLE_PERMANENT
)
from ..permissions import permission_users_impersonate

logger = logging.getLogger(name=__name__)


class ImpersonateMiddleware(MiddlewareMixin):
    @staticmethod
    def get_user(pk, request):
        return get_user_queryset().exclude(pk=request.user.pk).get(
            pk=pk
        )

    @staticmethod
    def permission_check(user):
        return Permission.check_user_permissions(
            permissions=(permission_users_impersonate,), user=user
        )

    def process_request(self, request):
        impersonate_permanent_session = IMPERSONATE_VARIABLE_PERMANENT in request.session

        if not impersonate_permanent_session:
            if IMPERSONATE_VARIABLE_DISABLE in request.POST or IMPERSONATE_VARIABLE_DISABLE in request.GET:
                if IMPERSONATE_VARIABLE_ID in request.session:
                    user_impersonated_id = request.session[IMPERSONATE_VARIABLE_ID]
                    del request.session[IMPERSONATE_VARIABLE_ID]

                    user_new = ImpersonateMiddleware.get_user(
                        pk=user_impersonated_id, request=request
                    )
                    event_user_impersonation_ended.commit(
                        actor=request.user, target=user_new
                    )
            else:
                impersonate_id = request.GET.get(
                    IMPERSONATE_VARIABLE_ID, request.POST.get(
                        IMPERSONATE_VARIABLE_ID
                    )
                )
                impersonate_permanent = IMPERSONATE_VARIABLE_PERMANENT in request.GET or IMPERSONATE_VARIABLE_PERMANENT in request.POST

                if impersonate_id:
                    try:
                        impersonate_id = int(impersonate_id)
                    except ValueError:
                        logger.error(
                            'Unable to impersonate, invalid user ID value. %s',
                            impersonate_id
                        )
                    else:
                        if ImpersonateMiddleware.permission_check(user=request.user):
                            request.session[IMPERSONATE_VARIABLE_ID] = impersonate_id

                            user_new = ImpersonateMiddleware.get_user(
                                pk=request.session[IMPERSONATE_VARIABLE_ID],
                                request=request
                            )
                            event_user_impersonation_started.commit(
                                actor=request.user, target=user_new
                            )

                            if impersonate_permanent:
                                request.session[IMPERSONATE_VARIABLE_PERMANENT] = True

        if IMPERSONATE_VARIABLE_ID in request.session and ImpersonateMiddleware.permission_check(user=request.user):
            request.user = ImpersonateMiddleware.get_user(
                pk=request.session[IMPERSONATE_VARIABLE_ID], request=request
            )
