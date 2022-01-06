from ..classes import MIMETypeBackend


class MIMETypeBackendMixin:
    def setUp(self):
        super().setUp()
        self.mime_type_backend = MIMETypeBackend.get_backend_instance()
