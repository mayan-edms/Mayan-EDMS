def condition_user_is_not_super_user(context, resolved_object):
    #TODO: Use a subclass test instead
    if hasattr(resolved_object, 'is_staff'):
        user = resolved_object
        return not user.is_superuser and not user.is_staff
    return True
