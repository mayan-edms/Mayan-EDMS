class CheckVersionViewTestMixin:
    def _request_check_version_view(self):
        return self.get(viewname='dependencies:check_version_view')
