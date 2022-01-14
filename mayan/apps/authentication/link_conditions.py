def condition_is_current_user(context, resolved_object):
    return condition_user_is_authenticated and resolved_object == context['request'].user


def condition_not_is_current_user(context, resolved_object):
    return condition_user_is_authenticated and not condition_is_current_user(
        context=context, resolved_object=resolved_object
    )


def condition_user_is_authenticated(context, resolved_object):
    if 'user' in context:
        return context['user'].is_authenticated
