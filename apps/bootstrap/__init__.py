from __future__ import absolute_import

from navigation.api import bind_links

from .links import bootstrap_execute
from .models import BootstrapSetup

bind_links([BootstrapSetup], [bootstrap_execute])
