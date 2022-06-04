def get_context_user(context):
    if 'user' in context:
        return context['user']
    elif 'request' in context:
        return getattr(context['request'], 'user', None)
