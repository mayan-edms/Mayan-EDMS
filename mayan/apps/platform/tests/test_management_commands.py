from io import StringIO

from django.core import management

from mayan.apps.tests.tests.base import BaseTestCase

from ..classes import PlatformTemplate

TEST_TEMPLATE_LABEL = 'test template label'
TEST_TEMPLATE_NAME = 'test_template_name'
TEST_TEMPLATE_STRING = '''
test template string
test template variable: {{ test_template_variable }}
'''
TEST_TEMPLATE_VARIABLE_VALUE = 'test_variable_value'
TEST_TEMPLATE_VARIABLE_VALUE_ALT = 'test_variable_value_alt'
TEST_TEMPLATE_STRING_RENDER = '''
test template string
test template variable: {}
'''.format(TEST_TEMPLATE_VARIABLE_VALUE)
TEST_TEMPLATE_STRING_RENDER_ALT = '''
test template string
test template variable: {}
'''.format(TEST_TEMPLATE_VARIABLE_VALUE_ALT)


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
