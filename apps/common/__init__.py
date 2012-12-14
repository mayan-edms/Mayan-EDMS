from __future__ import absolute_import

from django.conf import settings

from .debug import insert_pdb_exception_hook

if getattr(settings, 'DEBUG_ON_EXCEPTION', False):
    insert_pdb_exception_hook()
