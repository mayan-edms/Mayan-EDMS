from __future__ import absolute_import

import os
import glob

from django.utils.importlib import import_module
from django.conf import settings as django_settings

from .classes import Icon, IconSetBase

for app_name in django_settings.INSTALLED_APPS:
    try:
        sets_top = import_module('%s.iconsets' % app_name)
    except ImportError:
        pass
    else:
        for icon_set_name in [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(sets_top.__file__) + "/*.py")][1:]:
            icon_set_module = import_module('%s.iconsets.%s' % (app_name, icon_set_name))
            klass = getattr(icon_set_module, 'IconSet', None)
            if klass:
                klass()
