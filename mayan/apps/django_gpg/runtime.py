from __future__ import absolute_import

import sys

from .api import GPG
from .conf.settings import KEYSERVERS, GPG_HOME

try:
    gpg = GPG(home=GPG_HOME, keyservers=KEYSERVERS)
except Exception as exception:
    gpg = GPG(keyservers=KEYSERVERS)
    # TODO: Maybe raise a standard exception to signify configuration error
    sys.stderr.write(u'ERROR: GPG initialization error: %s\n' % exception)
    sys.stderr.write(u'INFO: Initializating GPG with system default home\n')
