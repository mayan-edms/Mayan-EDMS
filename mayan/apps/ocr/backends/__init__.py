from __future__ import absolute_import

import sys

from django.utils.importlib import import_module

from ..conf.settings import BACKEND


class BackendBase(object):
    def execute(input_filename, language=None):
        raise NotImplemented


def get_ocr_backend():
    """
    Return the OCR backend using the path specified in the configuration
    settings
    """
    try:
        module = import_module(BACKEND)
    except ImportError:
        sys.stderr.write(u'\nWarning: No OCR backend named: %s\n\n' % BACKEND)
        raise
    else:
        return module

ocr_backend = get_ocr_backend()
