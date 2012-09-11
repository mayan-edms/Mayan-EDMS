from __future__ import absolute_import

import sys

from .api import GPG
from .settings import KEYSERVERS, GPG_HOME

try:
    gpg = GPG(home=GPG_HOME, keyservers=KEYSERVERS)
except Exception, e:
    gpg = GPG(keyservers=KEYSERVERS)
    sys.stderr.write(u'ERROR: GPG initialization error: %s\n' % e)
    sys.stderr.write(u'INFO: Initializating GPG with system default home\n')
