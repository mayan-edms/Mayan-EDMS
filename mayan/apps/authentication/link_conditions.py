from .utils import get_context_user


def condition_is_current_user(context, resolved_object):
    if condition_user_is_authenticated(context=context, resolved_object=resolved_object):
        user = get_context_user(context=context)

        if user:
            return resolved_object == user


def condition_not_is_current_user(context, resolved_object):
    return condition_user_is_authenticated(
        context=context, resolved_object=resolved_object
    ) and not condition_is_current_user(
        context=context, resolved_object=resolved_object
    )


def condition_user_is_authenticated(context, resolved_object):
    user = get_context_user(context=context)

    if user:
        return user.is_authenticated
