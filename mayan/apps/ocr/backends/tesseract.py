from __future__ import unicode_literals

import codecs
import errno
import os
import subprocess
import tempfile

from common.utils import fs_cleanup

from . import BackendBase
from ..exceptions import OCRError
from ..settings import TESSERACT_PATH


class Tesseract(BackendBase):
    def execute(self, input_filename, language=None):
        """
        Execute the command line binary of tesseract
        """
        fd, filepath = tempfile.mkstemp()
        os.close(fd)
        ocr_output = os.extsep.join([filepath, 'txt'])
        command = [unicode(TESSERACT_PATH), unicode(input_filename), unicode(filepath)]

        if language is not None:
            command.extend(['-l', language])

        try:
            proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        except OSError as exception:
            if exception.errno == errno.ENOENT:
                raise OCRError('Tesseract not found at %s' % TESSERACT_PATH)
            else:
                raise
        else:
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
