from __future__ import unicode_literals

TEST_BODY_HTML = '<strong>test body</strong>'
TEST_EMAIL_ADDRESS = 'test@example.com'
TEST_RECIPIENTS_MULTIPLE_COMMA = 'test@example.com,test2@example.com'
TEST_RECIPIENTS_MULTIPLE_COMMA_RESULT = [
    'test@example.com', 'test2@example.com'
]
TEST_RECIPIENTS_MULTIPLE_SEMICOLON = 'test@example.com;test2@example.com'
TEST_RECIPIENTS_MULTIPLE_SEMICOLON_RESULT = [
    'test@example.com', 'test2@example.com'
]
TEST_RECIPIENTS_MULTIPLE_MIXED = 'test@example.com,test2@example.com;test2@example.com'
TEST_RECIPIENTS_MULTIPLE_MIXED_RESULT = [
    'test@example.com', 'test2@example.com', 'test2@example.com'
]
TEST_USER_MAILER_BACKEND_PATH = 'mailer.tests.mailers.TestBackend'
TEST_USER_MAILER_LABEL = 'test user mailer label'
