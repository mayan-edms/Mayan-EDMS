from __future__ import unicode_literals

from .literals import TEST_EMAIL_BASE64_FILENAME


class MockIMAPServer(object):
    def login(self, user, password):
        return ('OK', ['{} authenticated (Success)'.format(user)])

    def select(self, mailbox='INBOX', readonly=False):
        return ('OK', ['1'])

    def search(self, charset, *criteria):
        return ('OK', ['1'])

    def fetch(self, message_set, message_parts):
        return (
            'OK', [
                (
                    '1 (RFC822 {4800}',
                    TEST_EMAIL_BASE64_FILENAME
                ), ' FLAGS (\\Seen))'
            ]
        )

    def store(self, message_set, command, flags):
        return ('OK', ['1 (FLAGS (\\Seen \\Deleted))'])

    def expunge(self):
        return ('OK', ['1'])

    def close(self):
        return ('OK', ['Returned to authenticated state. (Success)'])

    def logout(self):
        return ('BYE', ['LOGOUT Requested'])
