from __future__ import absolute_import

import os

from .conf.settings import SUFFIX_SEPARATOR


def assemble_suffixed_filename(filename, suffix=0):
    """
    Split document filename, to attach suffix to the name part then
    re attacht the extension
    """

    if suffix:
        name, extension = filename.split(os.split(os.extsep))
        return SUFFIX_SEPARATOR.join([name, unicode(suffix), os.extsep, extension])
    else:
        return filename


def assemble_path_from_list(directory_list):
    return os.sep.join(directory_list)
