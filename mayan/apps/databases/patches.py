import datetime

from django.conf import settings
from django.db.migrations import Migration


def patch_Migration():
    _method_original__apply = Migration.apply
    _method_original__unapply = Migration.unapply

    def _method_patched__apply(self, *args, **kwargs):
        now_start = datetime.datetime.now()

        result = _method_original__apply(self, *args, **kwargs)

        time_delta = datetime.datetime.now() - now_start
        print(' (Time delta: {})'.format(time_delta), end='')
        return result

    def _method_patched__unapply(self, *args, **kwargs):
        now_start = datetime.datetime.now()

        result = _method_original__unapply(self, *args, **kwargs)

        time_delta = datetime.datetime.now() - now_start
        print(' (Time delta: {})'.format(time_delta), end='')
        return result

    if settings.DEBUG:
        Migration.apply = _method_patched__apply
        Migration.unapply = _method_patched__unapply
