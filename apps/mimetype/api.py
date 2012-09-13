import os

from django.conf import settings

try:
    import magic
    USE_PYTHON_MAGIC = True
except:
    import mimetypes
    mimetypes.init()
    USE_PYTHON_MAGIC = False


MIMETYPE_ICONS_DIRECTORY_NAME = os.path.join('images', 'mimetypes')

UNKNWON_TYPE_FILE_NAME = 'unknown.png'
ERROR_FILE_NAME = 'error.png'

mimetype_icons = {
    'application/pdf': 'file_extension_pdf.png',
    'application/zip': 'file_extension_zip.png',
    'application/ogg': 'file_extension_ogg.png',
    'application/postscript': 'file_extension_ps.png',
    'application/x-gzip': 'file_extension_gz.png',
    'application/x-rar-compressed': 'file_extension_rar.png',
    'application/x-troff-msvideo': 'file_extension_avi.png',
    'application/acad': 'file_extension_dwg.png',
    'application/octet-stream': 'file_extension_exe.png',
    'application/vnd.oasis.opendocument.text': 'ODF_textdocument_32x32.png',
    'application/vnd.oasis.opendocument.spreadsheet': 'ODF_spreadsheet_32x32.png',
    'application/vnd.oasis.opendocument.presentation': 'ODF_presentation_32x32.png',
    'application/vnd.oasis.opendocument.graphics': 'ODF_drawing_32x32.png',
    'application/vnd.ms-excel': 'file_extension_xls.png',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'file_extension_xls.png',
    'application/msword': 'file_extension_doc.png',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'file_extension_doc.png',
    'application/mspowerpoint': 'file_extension_pps.png',
    'application/vnd.ms-powerpoint': 'file_extension_pps.png',
    'application/wav': 'file_extension_wav.png',
    'application/x-wav': 'file_extension_wav.png',
    'application/vnd.oasis.opendocument.text': 'ODF_textdocument_32x32.png',

    'image/jpeg': 'file_extension_jpeg.png',
    'image/png': 'file_extension_png.png',
    'image/x-png': 'file_extension_png.png',
    'image/tiff': 'file_extension_tif.png',
    'image/x-tiff': 'file_extension_tif.png',
    'image/bmp': 'file_extension_bmp.png',
    'image/gif': 'file_extension_gif.png',
    'image/vnd.dwg': 'file_extension_dwg.png',
    'image/x-dwg': 'file_extension_dwg.png',

    'audio/mpeg': 'file_extension_mp3.png',
    'audio/mid': 'file_extension_mid.png',
    'audio/x-wav': 'file_extension_wav.png',
    'audio/vnd.wav': 'file_extension_wav.png',
    'audio/x-pn-realaudio': 'file_extension_ram.png',
    'audio/mp4': 'file_extension_mp4.png',
    'audio/x-ms-wma': 'file_extension_wma.png',

    'video/avi': 'file_extension_avi.png',
    'video/mpeg': 'file_extension_mpeg.png',
    'video/quicktime': 'file_extension_mov.png',
    'video/x-ms-asf': 'file_extension_asf.png',
    'video/x-ms-wmv': 'file_extension_wmv.png',

    'text/html': 'file_extension_html.png',
    'text/plain': 'file_extension_txt.png',
}


#def get_icon_file_path(mimetype):
#    file_name = mimetype_icons.get(mimetype, UNKNWON_TYPE_FILE_NAME)
#    if settings.DEVELOPMENT:
#        return os.path.join(settings.PROJECT_ROOT, 'apps', 'mimetype', 'static', MIMETYPE_ICONS_DIRECTORY_NAME, file_name)
#    else:
#        return os.path.join(settings.STATIC_ROOT, MIMETYPE_ICONS_DIRECTORY_NAME, file_name)


#def get_error_icon_file_path():
#    if settings.DEVELOPMENT:
#        return os.path.join(settings.PROJECT_ROOT, 'apps', 'mimetype', 'static', MIMETYPE_ICONS_DIRECTORY_NAME, ERROR_FILE_NAME)
#    else:
#        return os.path.join(settings.STATIC_ROOT, MIMETYPE_ICONS_DIRECTORY_NAME, ERROR_FILE_NAME)


#def get_error_icon_url():
#    return os.path.join(MIMETYPE_ICONS_DIRECTORY_NAME, ERROR_FILE_NAME)


def get_mimetype(file_description, filepath, mimetype_only=False):
    """
    Determine a file's mimetype by calling the system's libmagic
    library via python-magic or fallback to use python's mimetypes
    library
    """
    file_mimetype = None
    file_mime_encoding = None
    if USE_PYTHON_MAGIC:
        mime = magic.Magic(mime=True)
        file_mimetype = mime.from_buffer(file_description.read())
        if not mimetype_only:
            file_description.seek(0)
            mime_encoding = magic.Magic(mime_encoding=True)
            file_mime_encoding = mime_encoding.from_buffer(file_description.read())
    else:
        path, filename = os.path.split(filepath)
        file_mimetype, file_mime_encoding = mimetypes.guess_type(filename)

    file_description.close()

    return file_mimetype, file_mime_encoding
