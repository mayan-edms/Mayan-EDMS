import os
import subprocess
import hashlib

from mimetype.api import get_mimetype
from common.conf.settings import TEMPORARY_DIRECTORY

from converter.conf.settings import UNOCONV_PATH
from converter.exceptions import (OfficeConversionError,
    OfficeBackendError, UnknownFileFormat)

HASH_FUNCTION = lambda x: hashlib.sha256(x).hexdigest()

CACHED_FILE_SUFFIX = u'_office_converter'
    
CONVERTER_OFFICE_FILE_MIMETYPES = [
    'application/msword',
    'application/mswrite',
    'application/mspowerpoint',
    'application/msexcel',
    'application/vnd.ms-excel',
    'application/vnd.ms-powerpoint',    
    'text/plain',
    'application/vnd.oasis.opendocument.presentation',
]
#    'application/vnd.oasis.opendocument.text': 'ODF_textdocument_32x32.png',
#    'application/vnd.oasis.opendocument.spreadsheet': 'ODF_spreadsheet_32x32.png',
#    'application/vnd.oasis.opendocument.presentation': 'ODF_presentation_32x32.png',
#    'application/vnd.oasis.opendocument.graphics': 'ODF_drawing_32x32.png',
#    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'file_extension_xls.png',
#    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'file_extension_doc.png',
#    'application/vnd.oasis.opendocument.text': 'ODF_textdocument_32x32.png',

class OfficeConverter(object):
    def __init__(self, input_filepath):
        self.backend = OfficeConverterBackendUnoconv(unoconv_path=UNOCONV_PATH)
        self.input_filepath = input_filepath
        self.exists = False

        # Make sure file is of a known office format  
        descriptor = open(self.input_filepath)
        mimetype, encoding = get_mimetype(descriptor, self.input_filepath)

        if mimetype in CONVERTER_OFFICE_FILE_MIMETYPES:
            # Hash file to cache results of conversion
            #descriptor = open(self.input_filepath)
            #file_hash = HASH_FUNCTION(descriptor.read())
            #descriptor.close()
            
            #self.output_filepath = os.path.join(TEMPORARY_DIRECTORY, u''.join([file_hash, CACHED_FILE_SUFFIX]))
            self.output_filepath = os.path.join(TEMPORARY_DIRECTORY, u''.join([self.input_filepath, CACHED_FILE_SUFFIX]))
            self.exists = os.path.exists(self.output_filepath)
            print 'self.input_filepath',self.input_filepath
            print 'self.output_filepath',self.output_filepath
            print 'self.exists', self.exists
            if not self.exists:
                try:
                    self.backend.convert(self.input_filepath, self.output_filepath)
                except OfficeBackendError, msg:
                    print 'OFFICE EXCEPTION'
                    # convert exception so that atleas the mime type icon is displayed
                    raise UnknownFileFormat(msg)
        

        
    def __unicode__(self):
        return getattr(self, 'output_filepath', None)
        
    def __str__(self):
        return str(self.__unicode__())
                
    def __nonzero__(self):
        return self.exists

    __bool__ = __nonzero__
    

class OfficeConverterBackendUnoconv(object):
    def __init__(self, unoconv_path=None):
        self.unoconv_path = unoconv_path if unoconv_path else u'/usr/bin/unoconv'
        if not os.path.exists(self.unoconv_path):
            raise OfficeBackendError('cannot find unoconv executable')

    def convert(self, input_filepath, output_filepath):
        """
        Executes the program unoconv using subprocess's Popen
        """
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath
        
        command = []
        command.append(self.unoconv_path)
        #command.append(u'-v')
        command.append(u'--pipe')
        command.append(u'--format="pdf"')
        command.append(u'--output=%s' % self.output_filepath)
        command.append(self.input_filepath)
        print 'convert'
        try:
            proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            return_code = proc.wait()
            readline = proc.stderr.readline()
            if return_code != 0:
                raise OfficeBackendError(proc.stderr.readline())
        except OSError, msg:
            raise OfficeBackendError(msg)
