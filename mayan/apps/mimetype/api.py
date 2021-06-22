from .classes import MIMETypeBackend


def get_mimetype(file_object, mimetype_only=False):
    mime_type_backend = MIMETypeBackend.get_backend_instance()

    return mime_type_backend.get_mimetype(
        file_object=file_object, mimetype_only=mimetype_only
    )
