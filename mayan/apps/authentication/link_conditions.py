def condition_user_is_authenticated(context, resolved_object):
    # ~ if resolved_object:
        # ~ return resolved_object.is_authenticated()
    return context['user'].is_authenticated
    # ~ return resolved_object.is_authenticated()
