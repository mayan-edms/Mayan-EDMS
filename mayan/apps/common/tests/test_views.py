from mayan.apps.tests.tests.base import GenericViewTestCase


class CommonViewTestMixin:
    def _request_about_view(self):
        return self.get(viewname='common:about_view')


class CommonViewTestCase(CommonViewTestMixin, GenericViewTestCase):
    def test_about_view(self):
        response = self._request_about_view()
        self.assertContains(response=response, text='About', status_code=200)
