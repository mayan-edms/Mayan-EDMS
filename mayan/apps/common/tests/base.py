from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.template import Context, Template
from django.test import TestCase
from django.test.utils import ContextList
from django.urls import clear_url_caches, reverse

from django_downloadview import assert_download_response

from permissions.classes import Permission
from smart_settings.classes import Namespace
from user_management.tests import (
    TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME, TEST_USER_USERNAME,
    TEST_USER_PASSWORD
)

from .literals import TEST_VIEW_NAME, TEST_VIEW_URL
from .mixins import (
    ContentTypeCheckMixin, OpenFileCheckMixin, TempfileCheckMixin, UserMixin
)


class BaseTestCase(UserMixin, ContentTypeCheckMixin, OpenFileCheckMixin, TempfileCheckMixin, TestCase):
    """
    This is the most basic test case class any test in the project should use.
    """
    assert_download_response = assert_download_response

    def setUp(self):
        super(BaseTestCase, self).setUp()
        Namespace.invalidate_cache_all()
        Permission.invalidate_cache()


class GenericViewTestCase(BaseTestCase):
    def setUp(self):
        super(GenericViewTestCase, self).setUp()
        self.has_test_view = False

    def tearDown(self):
        from mayan.urls import urlpatterns

        self.client.logout()
        if self.has_test_view:
            urlpatterns.pop(0)
        super(GenericViewTestCase, self).tearDown()

    def add_test_view(self, test_object):
        from mayan.urls import urlpatterns

        def test_view(request):
            template = Template('{{ object }}')
            context = Context(
                {'object': test_object, 'resolved_object': test_object}
            )
            return HttpResponse(template.render(context=context))

        urlpatterns.insert(0, url(TEST_VIEW_URL, test_view, name=TEST_VIEW_NAME))
        clear_url_caches()
        self.has_test_view = True

    def get_test_view(self):
        response = self.get(TEST_VIEW_NAME)
        if isinstance(response.context, ContextList):
            # template widget rendering causes test client response to be
            # ContextList rather than RequestContext. Typecast to dictionary
            # before updating.
            result = dict(response.context).copy()
            result.update({'request': response.wsgi_request})
            return Context(result)
        else:
            response.context.update({'request': response.wsgi_request})
            return Context(response.context)

    def get(self, viewname=None, path=None, *args, **kwargs):
        data = kwargs.pop('data', {})
        follow = kwargs.pop('follow', False)

        if viewname:
            path = reverse(viewname=viewname, *args, **kwargs)

        return self.client.get(
            path=path, data=data, follow=follow
        )

    def login(self, username, password):
        logged_in = self.client.login(username=username, password=password)

        user = get_user_model().objects.get(username=username)

        self.assertTrue(logged_in)
        self.assertTrue(user.is_authenticated)

    def login_user(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

    def login_admin_user(self):
        self.login(username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD)

    def logout(self):
        self.client.logout()

    def post(self, viewname=None, path=None, *args, **kwargs):
        data = kwargs.pop('data', {})
        follow = kwargs.pop('follow', False)

        if viewname:
            path = reverse(viewname=viewname, *args, **kwargs)

        return self.client.post(
            path=path, data=data, follow=follow
        )
