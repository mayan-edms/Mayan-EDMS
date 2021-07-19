import glob
import importlib
import logging
import os
import random
import time

from furl import furl
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver

from django.apps import apps
from django.conf import settings
from django.conf.urls import url
from django.contrib.contenttypes.models import ContentType
from django.db import connection, connections, models
from django.db.models.signals import post_save, pre_save
from django.http import HttpResponse
from django.template import Context, Template
from django.test.utils import ContextList
from django.urls import clear_url_caches, reverse
from django.utils.encoding import DjangoUnicodeDecodeError, force_text

from stronghold.decorators import public

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.permissions.tests.mixins import PermissionTestMixin
from mayan.apps.storage.settings import setting_temporary_directory
from mayan.apps.views.compat import FileResponse

from ..literals import (
    TEST_SERVER_HOST, TEST_SERVER_SCHEME, TEST_VIEW_NAME, TEST_VIEW_URL
)


if getattr(settings, 'COMMON_TEST_FILE_HANDLES', False):
    import psutil


class ClientMethodsTestCaseMixin:
    def _build_verb_kwargs(self, viewname=None, path=None, *args, **kwargs):
        data = kwargs.pop('data', None) or {}
        follow = kwargs.pop('follow', False)
        query = kwargs.pop('query', None) or {}
        headers = kwargs.pop('headers', None) or {}

        if viewname:
            path = reverse(viewname=viewname, *args, **kwargs)

        path = furl(url=path)
        path.args.update(query)

        result = {'follow': follow, 'data': data, 'path': path.tostr()}
        result.update(headers)
        return result

    def delete(self, viewname=None, path=None, *args, **kwargs):
        return self.client.delete(
            **self._build_verb_kwargs(
                path=path, viewname=viewname, *args, **kwargs
            )
        )

    def generic(self, method, viewname=None, path=None, *args, **kwargs):
        return self.client.generic(
            method=method, **self._build_verb_kwargs(
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


class ConnectionsCheckTestCaseMixin:
    _open_connections_check_enable = True

    def _get_open_connections_count(self):
        return len(connections.all())

    def setUp(self):
        super().setUp()
        self._connections_count = self._get_open_connections_count()

    def tearDown(self):
        if self._open_connections_check_enable:

            self.assertEqual(
                self._connections_count, self._get_open_connections_count(),
                msg='Database connection leak. The number of database '
                'connections at the start and at the end of the test are not '
                'the same.'
            )

        super().tearDown()


class ContentTypeCheckTestCaseMixin:
    expected_content_types = ('text/html', 'text/html; charset=utf-8')

    def _pre_setup(self):
        super()._pre_setup()
        test_instance = self

        class CustomClient(self.client_class):
            def request(self, *args, **kwargs):
                response = super().request(*args, **kwargs)

                content_type = response._headers.get('content-type', [None, ''])[1]
                if test_instance.expected_content_types:
                    test_instance.assertTrue(
                        content_type in test_instance.expected_content_types,
                        msg='Unexpected response content type: {}, expected: {}.'.format(
                            content_type, ' or '.join(test_instance.expected_content_types)
                        )
                    )

                return response

        self.client = CustomClient()


class ContentTypeTestCaseMixin:
    def _inject_test_object_content_type(self):
        self.test_object_content_type = ContentType.objects.get_for_model(
            model=self.test_object
        )

        self.test_object_view_kwargs = {
            'app_label': self.test_object_content_type.app_label,
            'model_name': self.test_object_content_type.model,
            'object_id': self.test_object.pk
        }


class DelayTestCaseMixin:
    def _test_delay(self, seconds=0.1):
        time.sleep(seconds)


class DownloadTestCaseMixin:
    def assert_download_response(
        self, response, content=None, filename=None, is_attachment=None,
        mime_type=None
    ):
        self.assertTrue(isinstance(response, FileResponse))

        if filename:
            self.assertEqual(
                response[
                    'Content-Disposition'
                ].split('filename="')[1].split('"')[0], filename
            )

        if content:
            response_content = b''.join(list(response))

            try:
                response_content = force_text(s=response_content)
            except DjangoUnicodeDecodeError:
                """Leave as bytes"""

            self.assertEqual(response_content, content)

        if is_attachment is not None:
            self.assertEqual(response['Content-Disposition'], 'attachment')

        if mime_type:
            self.assertTrue(response['Content-Type'].startswith(mime_type))


class EnvironmentTestCaseMixin:
    def setUp(self):
        super().setUp()
        self._test_environment_variables = []

    def tearDown(self):
        for name in self._test_environment_variables:
            os.environ.pop(name)

        super().tearDown()

    def _set_environment_variable(self, name, value):
        self._test_environment_variables.append(name)
        os.environ[name] = value


class ModelTestCaseMixin:
    def _model_instance_to_dictionary(self, instance):
        return instance._meta.model._default_manager.filter(
            pk=instance.pk
        ).values()[0]


class OpenFileCheckTestCaseMixin:
    def _get_descriptor_count(self):
        process = psutil.Process()
        return process.num_fds()

    def _get_open_files(self):
        process = psutil.Process()
        return process.open_files()

    def setUp(self):
        super().setUp()
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

        super().tearDown()


class RandomPrimaryKeyModelMonkeyPatchMixin:
    random_primary_key_random_floor = 100
    random_primary_key_random_ceiling = 10000
    random_primary_key_maximum_attempts = 100
    random_primary_key_enable = True

    @staticmethod
    def get_unique_primary_key(model):
        manager = model._meta.default_manager

        attempts = 0
        while True:
            primary_key = random.randint(
                RandomPrimaryKeyModelMonkeyPatchMixin.random_primary_key_random_floor,
                RandomPrimaryKeyModelMonkeyPatchMixin.random_primary_key_random_ceiling
            )

            if not manager.filter(pk=primary_key).exists():
                break

            attempts = attempts + 1

            if attempts > RandomPrimaryKeyModelMonkeyPatchMixin.random_primary_key_maximum_attempts:
                raise Exception(
                    'Maximum number of retries for an unique random primary '
                    'key reached.'
                )

        return primary_key

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        random.seed()

    def setUp(self):
        if self.random_primary_key_enable:
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

                    kwargs['force_insert'] = True

                    result = instance.save_base(*args, **kwargs)
                    instance._meta.auto_created = False

                    post_save.send(
                        sender=instance.__class__, instance=instance, created=True,
                        update_fields=None, raw=False
                    )

                    return result

            setattr(models.Model, 'save', method_save_new)
        super().setUp()

    def tearDown(self):
        if self.random_primary_key_enable:
            models.Model.save = self.method_save_original
        super().tearDown()


class SeleniumTestMixin:
    SKIP_VARIABLE_NAME = 'TESTS_SELENIUM_SKIP'

    @staticmethod
    def _get_skip_variable_value():
        return os.environ.get(
            SeleniumTestMixin._get_skip_variable_environment_name(),
            getattr(settings, SeleniumTestMixin.SKIP_VARIABLE_NAME, False)
        )

    @staticmethod
    def _get_skip_variable_environment_name():
        return 'MAYAN_{}'.format(SeleniumTestMixin.SKIP_VARIABLE_NAME)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.webdriver = None
        if not SeleniumTestMixin._get_skip_variable_value():
            options = Options()
            options.add_argument('--headless')
            cls.webdriver = WebDriver(
                firefox_options=options, log_path='/dev/null'
            )

    @classmethod
    def tearDownClass(cls):
        if cls.webdriver:
            cls.webdriver.quit()
        super().tearDownClass()

    def setUp(self):
        if SeleniumTestMixin._get_skip_variable_value():
            self.skipTest(reason='Skipping selenium test')
        super().setUp()

    def _open_url(self, fragment=None, path=None, viewname=None):
        url = '{}{}{}'.format(
            self.live_server_url, path or reverse(viewname=viewname),
            fragment or ''
        )

        self.webdriver.get(url=url)


class SilenceLoggerTestCaseMixin:
    """
    Changes the log level of a specific logger for the duration of a test.
    The default level for silenced loggers is CRITICAL.
    Example: self._silence_logger(name='mayan.apps.converter.managers')
    """
    test_case_silenced_logger = None
    test_case_silenced_logger_new_level = logging.CRITICAL

    def tearDown(self):
        if self.test_case_silenced_logger:
            self.test_case_silenced_logger.setLevel(
                level=self.test_case_silenced_logger_level
            )

        super().tearDown()

    def _silence_logger(self, name):
        self.test_case_silenced_logger = logging.getLogger(name=name)
        self.test_case_silenced_logger_level = self.test_case_silenced_logger.level
        self.test_case_silenced_logger.setLevel(
            level=self.test_case_silenced_logger_new_level
        )


class TempfileCheckTestCasekMixin:
    # Ignore the jvmstat instrumentation and GitLab's CI .config files.
    # Ignore LibreOffice fontconfig cache dir.
    ignore_globs = ('hsperfdata_*', '.config', '.cache')

    def _get_temporary_entries(self):
        ignored_result = []

        # Expand globs by joining the temporary directory and then flattening
        # the list of lists into a single list.
        for item in self.ignore_globs:
            ignored_result.extend(
                glob.glob(
                    os.path.join(setting_temporary_directory.value, item)
                )
            )

        # Remove the path and leave only the expanded filename.
        ignored_result = map(lambda x: os.path.split(x)[-1], ignored_result)

        return set(
            os.listdir(setting_temporary_directory.value)
        ) - set(ignored_result)

    def setUp(self):
        super().setUp()
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
        super().tearDown()


class TestModelTestCaseMixin(ContentTypeTestCaseMixin, PermissionTestMixin):
    auto_create_test_object = False
    auto_create_test_object_fields = None
    auto_create_test_object_instance_kwargs = None
    auto_create_test_object_permission = False

    @classmethod
    def setUpClass(cls):
        if connection.vendor == 'sqlite':
            connection.disable_constraint_checking()

        super().setUpClass()

    def setUp(self):
        self._test_models = []
        self.test_objects = []

        super().setUp()

        if self.auto_create_test_object:
            self._create_test_object(
                fields=self.auto_create_test_object_fields,
                create_test_permission=self.auto_create_test_object_permission,
                instance_kwargs=self.auto_create_test_object_instance_kwargs
            )

    def tearDown(self):
        # Delete the test models' content type entries and deregister the
        # permissions, this avoids their Content Type from being looked up
        # in subsequent tests where they don't exists due to the database
        # transaction rollback.
        for model in self._test_models:
            content_type = ContentType.objects.get_for_model(model=model)
            if content_type.pk:
                content_type.delete()
            ModelPermission.deregister(model=model)

        super().tearDown()

    def _create_test_model(
        self, base_class=models.Model, fields=None, model_name=None,
        options=None
    ):
        test_model_count = len(self._test_models)
        self._test_model_name = model_name or '{}_{}'.format(
            'TestModel', test_model_count
        )

        self.options = options
        # Obtain the app_config and app_label from the test's module path.
        self.app_config = apps.get_containing_app_config(
            object_name=self.__class__.__module__
        )

        if connection.vendor == 'mysql':
            self.skipTest(
                reason='MySQL doesn\'t support schema changes inside an '
                'atomic block.'
            )

        attrs = {
            '__module__': self.__class__.__module__,
            'save': self._get_test_model_save_method(),
            'Meta': self._get_test_model_meta(),
        }

        if fields:
            attrs.update(fields)

        # Clear previous model registration before re-registering it again to
        # avoid conflict with test models with the same name, in the same app
        # but from another test module.
        apps.all_models[self.app_config.label].pop(
            self._test_model_name.lower(), None
        )

        model = type(
            self._test_model_name, (base_class,), attrs
        )

        if not model._meta.proxy:
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(model=model)

        self._test_models.append(model)
        ContentType.objects.clear_cache()

        return model

    def _create_test_object(
        self, fields=None, model_name=None, create_test_permission=False,
        instance_kwargs=None
    ):
        instance_kwargs = instance_kwargs or {}

        self.TestModel = self._create_test_model(
            fields=fields, model_name=model_name
        )
        self.test_object = self.TestModel.objects.create(**instance_kwargs)
        self._inject_test_object_content_type()

        if create_test_permission:
            self._create_test_permission()

            ModelPermission.register(
                model=self.TestModel, permissions=(
                    self.test_permission,
                )
            )

        self.test_objects.append(self.test_object)

    def _get_test_model_meta(self):
        self._test_db_table = '{}_{}'.format(
            self.app_config.label, self._test_model_name.lower()
        )

        class Meta:
            app_label = self.app_config.label
            db_table = self._test_db_table
            verbose_name = self._test_model_name

        if self.options:
            for key, value in self.options.items():
                setattr(Meta, key, value)

        return Meta

    def _get_test_model_save_method(self):
        def save(instance, *args, **kwargs):
            # Custom .save() method to use random primary key values.
            if instance.pk:
                return models.Model.self(instance, *args, **kwargs)
            else:
                instance.pk = RandomPrimaryKeyModelMonkeyPatchMixin.get_unique_primary_key(
                    model=instance._meta.model
                )
                instance.id = instance.pk

                kwargs['force_insert'] = True
                return instance.save_base(*args, **kwargs)
        return save


class TestServerTestCaseMixin:
    def setUp(self):
        super().setUp()
        self.testserver_prefix = self.get_testserver_prefix()
        self.testserver_url = self.get_testserver_url()
        self.test_view_request = None

    def _test_view_factory(self, test_object=None):
        def test_view(request):
            self.test_view_request = request
            return HttpResponse()

        return test_view

    def get_testserver_prefix(self):
        return furl(
            scheme=TEST_SERVER_SCHEME, host=TEST_SERVER_HOST,
        ).tostr()

    def get_testserver_url(self):
        return furl(
            scheme=TEST_SERVER_SCHEME, host=TEST_SERVER_HOST,
            path=self.test_view_url
        ).tostr()


class TestViewTestCaseMixin:
    auto_add_test_view = False
    has_test_view = False
    test_view_is_public = False
    test_view_object = None
    test_view_name = TEST_VIEW_NAME
    test_view_template = '{{ object }}'
    test_view_url = TEST_VIEW_URL

    def setUp(self):
        super().setUp()
        if self.auto_add_test_view:
            self.add_test_view(test_object=self.test_view_object)

    def tearDown(self):
        urlconf = importlib.import_module(settings.ROOT_URLCONF)

        self.client.logout()
        if self.has_test_view:
            urlconf.urlpatterns.pop(0)
        super().tearDown()

    def _get_context_from_test_response(self, response):
        if isinstance(response.context, ContextList):
            # Template widget rendering causes test client response to be
            # ContextList rather than RequestContext. Typecast to dictionary
            # before updating.
            result = dict(response.context).copy()
            result.update({'request': response.wsgi_request})
            context = Context(result)
        else:
            result = response.context or {}
            result.update({'request': response.wsgi_request})
            context = Context(result)

        context.request = response.wsgi_request
        return context

    def _test_view_factory(self, test_object=None):
        def test_view(request):
            template = Template(template_string=self.test_view_template)
            context = Context(
                dict_={'object': test_object, 'resolved_object': test_object}
            )
            return HttpResponse(content=template.render(context=context))

        if self.test_view_is_public:
            return public(function=test_view)
        else:
            return test_view

    def add_test_view(self, test_object=None):
        urlconf = importlib.import_module(settings.ROOT_URLCONF)

        urlconf.urlpatterns.insert(
            0, url(
                regex=self.test_view_url, view=self._test_view_factory(
                    test_object=test_object
                ), name=self.test_view_name
            )
        )
        clear_url_caches()
        self.has_test_view = True

    def get_test_view(self):
        response = self.get(viewname=self.test_view_name)
        return self._get_context_from_test_response(response=response)
