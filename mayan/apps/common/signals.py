from __future__ import unicode_literals

from django.dispatch import Signal

perform_upgrade = Signal(use_caching=True)
post_initial_setup = Signal(use_caching=True)
post_upgrade = Signal(use_caching=True)
