from django.template import Library

from ..literals import (
    USER_IMPERSONATE_VARIABLE_ID, USER_IMPERSONATE_VARIABLE_PERMANENT
)

register = Library()


@register.simple_tag(takes_context=True)
def authentication_impersonation_check(context):
    request = getattr(context, 'request', None)

    if request:
        user_id = request.session.get(USER_IMPERSONATE_VARIABLE_ID)
        impersonate_permanent_session = USER_IMPERSONATE_VARIABLE_PERMANENT in request.session

        if user_id and not impersonate_permanent_session:
            return context.request.user
        else:
            return False
    else:
        return False
