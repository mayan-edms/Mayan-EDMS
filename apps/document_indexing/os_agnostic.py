import os

from document_indexing.conf.settings import SUFFIX_SEPARATOR


def assemble_document_filename(filename, suffix=0):
    '''
    Split document filename, to attach suffix to the name part then
    re attacht the extension
    '''
    
    if suffix:
        name, extension = filename.split(os.split(os.extsep))
        return SUFFIX_SEPARATOR.join([name, unicode(suffix), os.extsep, extension])
    else:
        return file_filename
