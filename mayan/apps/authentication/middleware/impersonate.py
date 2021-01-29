import logging

from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin

from mayan.apps.acls.models import AccessControlList
from mayan.apps.user_management.querysets import get_user_queryset

from ..events import (
    event_user_impersonation_ended, event_user_impersonation_started
)
from ..literals import (
    USER_IMPERSONATE_VARIABLE_ID, USER_IMPERSONATE_VARIABLE_DISABLE,
    USER_IMPERSONATE_VARIABLE_PERMANENT
)
from ..permissions import permission_users_impersonate

logger = logging.getLogger(name=__name__)


class ImpersonateMiddleware(MiddlewareMixin):
    @staticmethod
    def get_user(pk, request):
        queryset = AccessControlList.objects.restrict_queryset(
            queryset=get_user_queryset().exclude(pk=request.user.pk),
            permission=permission_users_impersonate, user=request.user
        )

        return queryset.get(pk=pk)

    def process_request(self, request):
        User = get_user_model()

        impersonate_permanent_session = USER_IMPERSONATE_VARIABLE_PERMANENT in request.session

        if not impersonate_permanent_session:
            if USER_IMPERSONATE_VARIABLE_DISABLE in request.POST or USER_IMPERSONATE_VARIABLE_DISABLE in request.GET:
                # End the impersonation
                if USER_IMPERSONATE_VARIABLE_ID in request.session:
                    user_impersonate_id = request.session[USER_IMPERSONATE_VARIABLE_ID]

                    del request.session[USER_IMPERSONATE_VARIABLE_ID]

                    try:
                        user = ImpersonateMiddleware.get_user(
                            pk=user_impersonate_id, request=request
                        )
                    except User.DoesNotExist:
                        return
                    else:
                        event_user_impersonation_ended.commit(
                            actor=request.user, target=user
                        )
                        return
            else:
                # Start the impersonation
                user_impersonate_id = request.GET.get(
                    USER_IMPERSONATE_VARIABLE_ID, request.POST.get(
                        USER_IMPERSONATE_VARIABLE_ID
                    )
                )
                user_impersonate_permanent = USER_IMPERSONATE_VARIABLE_PERMANENT in request.GET or USER_IMPERSONATE_VARIABLE_PERMANENT in request.POST

                if user_impersonate_id:
                    try:
                        user_impersonate_id = int(user_impersonate_id)
                    except ValueError:
                        logger.error(
                            'Unable to impersonate, invalid user ID value. %s',
                            user_impersonate_id
                        )
                    else:
                        try:
                            user = ImpersonateMiddleware.get_user(
                                pk=user_impersonate_id, request=request
                            )
                        except User.DoesNotExist:
                            return
                        else:
                            request.session[USER_IMPERSONATE_VARIABLE_ID] = user_impersonate_id

                            event_user_impersonation_started.commit(
                                actor=request.user, target=user
                            )

                            request.user = user

                            if user_impersonate_permanent:
                                request.session[USER_IMPERSONATE_VARIABLE_PERMANENT] = True

                            return

        # Set the request user to the previously impersonated user.
        if USER_IMPERSONATE_VARIABLE_ID in request.session:
            user_impersonate_id = request.session[USER_IMPERSONATE_VARIABLE_ID]
            try:
                user = ImpersonateMiddleware.get_user(
                    pk=user_impersonate_id, request=request
                )
            except User.DoesNotExist:
                del request.session[USER_IMPERSONATE_VARIABLE_ID]
                return
            else:
                request.user = user
