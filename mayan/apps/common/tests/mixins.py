from __future__ import unicode_literals

import glob
import importlib
import os
import random

from furl import furl

from django.conf import settings
from django.conf.urls import url
from django.core import management
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.http import HttpResponse
from django.template import Context, Template
from django.test.utils import ContextList
from django.urls import clear_url_caches, reverse

from .literals import TEST_VIEW_NAME, TEST_VIEW_URL

from ..settings import setting_temporary_directory

if getattr(settings, 'COMMON_TEST_FILE_HANDLES', False):
    import psutil


class ClientMethodsTestCaseMixin(object):
    def _build_verb_kwargs(self, viewname=None, path=None, *args, **kwargs):
        data = kwargs.pop('data', {})
        follow = kwargs.pop('follow', False)
        query = kwargs.pop('query', {})

        if viewname:
            path = reverse(viewname=viewname, *args, **kwargs)

        path = furl(url=path)
        path.args.update(query)

        return {'follow': follow, 'data': data, 'path': path.tostr()}

    def delete(self, viewname=None, path=None, *args, **kwargs):
        return self.client.delete(
            **self._build_verb_kwargs(
                path=path, viewname=viewname, *args, **kwargs
            )
        )

    def get(self, viewname=None, path=None, *args, **kwargs):
        return self.client.get(
            **self._build_verb_kwargs(
                path=path, viewname=viewname, *args, **kwargs
            )
        )

    def patch(self, viewname=None, path=None, *args, **kwargs):
        return self.client.patch(
            **self._build_verb_kwargs(
                path=path, viewname=viewname, *args, **kwargs
            )
        )

    def post(self, viewname=None, path=None, *args, **kwargs):
        return self.client.post(
            **self._build_verb_kwargs(
                path=path, viewname=viewname, *args, **kwargs
            )
        )

    def put(self, viewname=None, path=None, *args, **kwargs):
        return self.client.put(
            **self._build_verb_kwargs(
                path=path, viewname=viewname, *args, **kwargs
            )
        )


class ContentTypeCheckTestCaseMixin(object):
    expected_content_type = 'text/html; charset=utf-8'

    def _pre_setup(self):
        super(ContentTypeCheckTestCaseMixin, self)._pre_setup()
        test_instance = self

        class CustomClient(self.client_class):
            def request(self, *args, **kwargs):
                response = super(CustomClient, self).request(*args, **kwargs)

                content_type = response._headers.get('content-type', [None, ''])[1]
                if test_instance.expected_content_type:
                    test_instance.assertEqual(
                        content_type, test_instance.expected_content_type,
                        msg='Unexpected response content type: {}, expected: {}.'.format(
                            content_type, test_instance.expected_content_type
                        )
                    )

                return response

        self.client = CustomClient()


class DatabaseConversionMixin(object):
    def _test_database_conversion(self, *app_labels):
        management.call_command(
            'convertdb', *app_labels, force=True
        )


class OpenFileCheckTestCaseMixin(object):
    def _get_descriptor_count(self):
        process = psutil.Process()
        return process.num_fds()

    def _get_open_files(self):
        process = psutil.Process()
        return process.open_files()

    def setUp(self):
        super(OpenFileCheckTestCaseMixin, self).setUp()
        if getattr(settings, 'COMMON_TEST_FILE_HANDLES', False):
            self._open_files = self._get_open_files()

    def tearDown(self):
        if getattr(settings, 'COMMON_TEST_FILE_HANDLES', False) and not getattr(self, '_skip_file_descriptor_test', False):
            for new_open_file in self._get_open_files():
                self.assertFalse(
                    new_open_file not in self._open_files,
                    msg='File descriptor leak. The number of file descriptors '
                    'at the start and at the end of the test are not the same.'
                )

            self._skip_file_descriptor_test = False

        super(OpenFileCheckTestCaseMixin, self).tearDown()


class RandomPrimaryKeyModelMonkeyPatchMixin(object):
    random_primary_key_random_floor = 100
    random_primary_key_random_ceiling = 10000
    random_primary_key_maximum_attempts = 100

    @staticmethod
    def get_unique_primary_key(model):
        pk_list = model._meta.default_manager.values_list('pk', flat=True)

        attempts = 0
        while True:
            primary_key = random.randint(
                RandomPrimaryKeyModelMonkeyPatchMixin.random_primary_key_random_floor,
                RandomPrimaryKeyModelMonkeyPatchMixin.random_primary_key_random_ceiling
            )

            if primary_key not in pk_list:
                break

            attempts = attempts + 1

            if attempts > RandomPrimaryKeyModelMonkeyPatchMixin.random_primary_key_maximum_attempts:
                raise Exception(
                    'Maximum number of retries for an unique random primary '
                    'key reached.'
                )

        return primary_key

    def setUp(self):
        self.method_save_original = models.Model.save

        def method_save_new(instance, *args, **kwargs):
            if instance.pk:
                return self.method_save_original(instance, *args, **kwargs)
            else:
                # Set meta.auto_created to True to have the original save_base
                # not send the pre_save signal which would normally send
                # the instance without a primary key. Since we assign a random
                # primary key any pre_save signal handler that relies on an
                # empty primary key will fail.
                # The meta.auto_created and manual pre_save sending emulates
                # the original behavior. Since meta.auto_created also disables
                # the post_save signal we must also send it ourselves.
                # This hack work with Django 1.11 .save_base() but can break
                # in future versions if that method is updated.
                pre_save.send(
                    sender=instance.__class__, instance=instance, raw=False,
                    update_fields=None,
                )
                instance._meta.auto_created = True
                instance.pk = RandomPrimaryKeyModelMonkeyPatchMixin.get_unique_primary_key(
                    model=instance._meta.model
                )
                instance.id = instance.pk

                result = instance.save_base(force_insert=True)
                instance._meta.auto_created = False

                post_save.send(
                    sender=instance.__class__, instance=instance, created=True,
                    update_fields=None, raw=False
                )

                return result

        setattr(models.Model, 'save', method_save_new)
        super(RandomPrimaryKeyModelMonkeyPatchMixin, self).setUp()

    def tearDown(self):
        models.Model.save = self.method_save_original
        super(RandomPrimaryKeyModelMonkeyPatchMixin, self).tearDown()


class TempfileCheckTestCasekMixin(object):
    # Ignore the jvmstat instrumentation and GitLab's CI .config files
    # Ignore LibreOffice fontconfig cache dir
    ignore_globs = ('hsperfdata_*', '.config', '.cache')

    def _get_temporary_entries(self):
        ignored_result = []

        # Expand globs by joining the temporary directory and then flattening
        # the list of lists into a single list
        for item in self.ignore_globs:
            ignored_result.extend(
                glob.glob(
                    os.path.join(setting_temporary_directory.value, item)
                )
            )

        # Remove the path and leave only the expanded filename
        ignored_result = map(lambda x: os.path.split(x)[-1], ignored_result)

        return set(
            os.listdir(setting_temporary_directory.value)
        ) - set(ignored_result)

    def setUp(self):
        super(TempfileCheckTestCasekMixin, self).setUp()
        if getattr(settings, 'COMMON_TEST_TEMP_FILES', False):
            self._temporary_items = self._get_temporary_entries()

    def tearDown(self):
        if getattr(settings, 'COMMON_TEST_TEMP_FILES', False):
            final_temporary_items = self._get_temporary_entries()
            self.assertEqual(
                self._temporary_items, final_temporary_items,
                msg='Orphan temporary file. The number of temporary files and/or '
                'directories at the start and at the end of the test are not the '
                'same. Orphan entries: {}'.format(
                    ','.join(final_temporary_items - self._temporary_items)
                )
            )
        super(TempfileCheckTestCasekMixin, self).tearDown()


class TestViewTestCaseMixin(object):
    has_test_view = False

    def tearDown(self):
        urlconf = importlib.import_module(settings.ROOT_URLCONF)

        self.client.logout()
        if self.has_test_view:
            urlconf.urlpatterns.pop(0)
        super(TestViewTestCaseMixin, self).tearDown()

    def add_test_view(self, test_object):
        urlconf = importlib.import_module(settings.ROOT_URLCONF)

        def test_view(request):
            template = Template('{{ object }}')
            context = Context(
                {'object': test_object, 'resolved_object': test_object}
            )
            return HttpResponse(template.render(context=context))

        urlconf.urlpatterns.insert(0, url(TEST_VIEW_URL, test_view, name=TEST_VIEW_NAME))
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
