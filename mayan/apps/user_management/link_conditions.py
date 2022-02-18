def condition_user_is_not_superuser(context, resolved_object):
    return not condition_user_is_superuser(
        context=context, resolved_object=resolved_object
    )


def condition_user_is_superuser(context, resolved_object):
    is_staff = getattr(resolved_object, 'is_staff', False)
    is_superuser = getattr(resolved_object, 'is_superuser', False)
    return is_staff or is_superuser
