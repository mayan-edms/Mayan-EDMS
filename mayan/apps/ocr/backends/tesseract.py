from __future__ import absolute_import

import codecs
import os
import subprocess
import tempfile

from common.utils import fs_cleanup

from . import BackendBase
from ..conf.settings import TESSERACT_PATH
from ..exceptions import OCRError


class Tesseract(BackendBase):
    def execute(self, input_filename, language=None):
        """
        Execute the command line binary of tesseract
        """
        fd, filepath = tempfile.mkstemp()
        os.close(fd)
        ocr_output = os.extsep.join([filepath, u'txt'])
        command = [unicode(TESSERACT_PATH), unicode(input_filename), unicode(filepath)]

        if language is not None:
            command.extend([u'-l', language])

        proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        return_code = proc.wait()
        if return_code != 0:
            error_text = proc.stderr.read()
            fs_cleanup(filepath)
            fs_cleanup(ocr_output)
            if language:
                # If tesseract gives an error with a language parameter
                # re-run it with no parameter again
                return self.execute(input_filename, language=None)
            else:
                raise OCRError(error_text)

        fd = codecs.open(ocr_output, 'r', 'utf-8')
        text = fd.read().strip()
        fd.close()

        os.unlink(filepath)

        return text
