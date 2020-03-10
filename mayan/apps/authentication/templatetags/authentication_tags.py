from __future__ import unicode_literals

from django.template import Library

from ..literals import (
    IMPERSONATE_VARIABLE_ID, IMPERSONATE_VARIABLE_PERMANENT
)

register = Library()


@register.simple_tag(takes_context=True)
def authentication_impersonation_check(context):
    user_id = context.request.session.get(IMPERSONATE_VARIABLE_ID)
    impersonate_permanent_session = IMPERSONATE_VARIABLE_PERMANENT in context.request.session

    if user_id and not impersonate_permanent_session:
        return context.request.user
    else:
        return False
