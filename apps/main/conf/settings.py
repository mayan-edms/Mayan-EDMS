from django.conf import settings

SIDE_BAR_SEARCH = getattr(settings, 'MAIN_SIDE_BAR_SEARCH', False)
