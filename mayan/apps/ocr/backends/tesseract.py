from __future__ import absolute_import

import codecs
import os
import subprocess
import tempfile
import sys

from . import BackendBase
from ..conf.settings import TESSERACT_PATH


def Tesseract(BackendBase):
    def execute(input_filename, language=None):
        """
        Execute the command line binary of tesseract
        """
        fd, filepath = tempfile.mkstemp()
        os.close(fd)
        ocr_output = os.extsep.join([filepath, u'txt'])
        command = [unicode(TESSERACT_PATH), unicode(input_filename), unicode(filepath)]

        if lang is not None:
            command.extend([u'-l', language])

        proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        return_code = proc.wait()
        if return_code != 0:
            error_text = proc.stderr.read()
            cleanup(filepath)
            cleanup(ocr_output)
            if lang:
                # If tesseract gives an error with a language parameter
                # re-run it with no parameter again
                return run_tesseract(input_filename, language=None)
            else:
                raise TesseractError(error_text)

        fd = codecs.open(ocr_output, 'r', 'utf-8')
        text = fd.read().strip()
        fd.close()

        os.unlink(filepath)

        return text
