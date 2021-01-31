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
