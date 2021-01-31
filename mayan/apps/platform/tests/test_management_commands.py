from io import StringIO

from django.core import management

from mayan.apps.testing.tests.base import BaseTestCase

from ..classes import PlatformTemplate

from .literals import (
    TEST_TEMPLATE_LABEL, TEST_TEMPLATE_NAME, TEST_TEMPLATE_STRING,
    TEST_TEMPLATE_STRING_RENDER, TEST_TEMPLATE_STRING_RENDER_ALT,
    TEST_TEMPLATE_VARIABLE_VALUE, TEST_TEMPLATE_VARIABLE_VALUE_ALT
)


class TestPlatformTemplate(PlatformTemplate):
    context = {'test_template_variable': TEST_TEMPLATE_VARIABLE_VALUE}
    label = TEST_TEMPLATE_LABEL
    name = TEST_TEMPLATE_NAME
    template_string = TEST_TEMPLATE_STRING


PlatformTemplate.register(klass=TestPlatformTemplate)


class PlatformTemplateManagementCommandTestCase(BaseTestCase):
    def test_platform_template_simple(self):
        output = StringIO()
        args = (TEST_TEMPLATE_NAME,)
        options = {
            'stdout': output
        }
        management.call_command('platformtemplate', *args, **options)
        self.assertEqual(output.getvalue(), TEST_TEMPLATE_STRING_RENDER)

    def test_platform_template_context(self):
        output = StringIO()
        args = (
            TEST_TEMPLATE_NAME, '--context',
            'test_template_variable: {}'.format(
                TEST_TEMPLATE_VARIABLE_VALUE_ALT
            )
        )
        options = {
            'stdout': output
        }
        management.call_command('platformtemplate', *args, **options)
        self.assertEqual(output.getvalue(), TEST_TEMPLATE_STRING_RENDER_ALT)
