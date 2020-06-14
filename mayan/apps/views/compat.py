import os
from urllib.parse import quote

from django.conf import settings
from django.http.response import FileResponse as DjangoFileResponse

from mayan.apps.mimetype.api import get_mimetype


class FileResponse(DjangoFileResponse):
    """
    Subclass of Django's 2.2 FileResponse
    Modified to allows downloading non file like content as attachment
    A streaming HTTP response class optimized for files.
    """
    def _set_as_attachment(self, filename):
        if self.as_attachment:
            filename = self.filename or os.path.basename(filename)
            if filename:
                try:
                    filename.encode('ascii')
                    file_expr = 'filename="{}"'.format(filename)
                except UnicodeEncodeError:
                    file_expr = "filename*=utf-8''{}".format(quote(filename))
                self['Content-Disposition'] = 'attachment; {}'.format(file_expr)

    def _set_streaming_content(self, value):
        if not hasattr(value, 'read'):
            self.file_to_stream = None
            result = super(FileResponse, self)._set_streaming_content(value)
            self._set_as_attachment(filename=self.filename)

            return result

        self.file_to_stream = filelike = value
        if hasattr(filelike, 'close'):
            self._closable_objects.append(filelike)
        value = iter(lambda: filelike.read(self.block_size), b'')
        self.set_headers(filelike)
        super(FileResponse, self)._set_streaming_content(value)

    def set_headers(self, filelike):
        """
        Set some common response headers (Content-Length, Content-Type, and
        Content-Disposition) based on the `filelike` response content.
        """
        encoding_map = {
            'bzip2': 'application/x-bzip',
            'gzip': 'application/gzip',
            'xz': 'application/x-xz',
        }
        filename = getattr(filelike, 'name', None)
        filename = filename if (isinstance(filename, str) and filename) else self.filename
        if os.path.isabs(filename):
            self['Content-Length'] = os.path.getsize(filelike.name)
        elif hasattr(filelike, 'getbuffer'):
            self['Content-Length'] = filelike.getbuffer().nbytes

        if self.get('Content-Type', '').startswith(settings.DEFAULT_CONTENT_TYPE):
            if self.file_to_stream:
                content_type, encoding = get_mimetype(
                    file_object=self.file_to_stream, mimetype_only=True
                )
                # Encoding isn't set to prevent browsers from automatically
                # uncompressing files.
                content_type = encoding_map.get(encoding, content_type)
                self['Content-Type'] = content_type or 'application/octet-stream'
            else:
                self['Content-Type'] = 'application/octet-stream'

        self._set_as_attachment(filename=filename)
