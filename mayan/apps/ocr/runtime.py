from __future__ import absolute_import

from common.utils import load_backend

from .conf.settings import BACKEND, LANGUAGE

try:
    language_backend = load_backend(u'.'.join([u'ocr', u'lang', LANGUAGE, u'LanguageBackend']))()
except ImportError:
    language_backend = None

ocr_backend = load_backend(BACKEND)()
