def condition_user_is_authenticated(context, resolved_object):
    if 'user' in context:
        return context['user'].is_authenticated
