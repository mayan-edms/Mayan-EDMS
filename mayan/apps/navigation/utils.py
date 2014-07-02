from django.core.urlresolvers import resolve


def resolve_to_name(path, urlconf=None):
    return resolve(path, urlconf=urlconf).view_name
