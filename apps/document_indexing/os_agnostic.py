from document_indexing.conf.settings import SUFFIX_SEPARATOR


def assemble_document_filename(document, suffix=0):
    if suffix:
        return SUFFIX_SEPARATOR.join([document.file_filename, unicode(suffix)])
    else:
        return document.file_filename
