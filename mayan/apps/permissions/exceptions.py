from django.core.exceptions import PermissionDenied as DjangoPermissionDenied


class PermissionDenied(DjangoPermissionDenied):
    pass
