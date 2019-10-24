from __future__ import unicode_literals


class MockIMAPMessage(object):
    flags = []
    uid = None

    def __init__(self):
        self.uid = '999'

    def get_flags(self):
        return ' '.join(self.flags)


class MockIMAPMailbox(object):
    messages = []

    def __init__(self, name='INBOX'):
        self.name = name


class MockIMAPServer(object):
    def __init__(self):
        self.mailboxes = {
            'INBOX': MockIMAPMailbox(name='INBOX')
        }
        self.mailboxes['INBOX'].messages.append(MockIMAPMessage())
        self.mailbox_selected = None

    def close(self):
        return ('OK', ['Returned to authenticated state. (Success)'])

    def expunge(self):
        result = []

        for message in self.mailbox_selected.messages:
            if '\\Deleted' in message.flags:
                result.append(
                    force_text(
                        self.mailbox_selected.messages.index(message)
                    )
                )
                self.mailbox_selected.messages.remove(message)

        return ('OK', ' '.join(result))

    def fetch(self, message_set, message_parts):
        results = []
        for message_number in message_set.split():
            message = self.mailbox_selected.messages[int(message_number) - 1]
            if '\\Seen' not in message.flags:
                message.flags.append('\\Seen')

            results.append(
                (
                    '{} (RFC822 {{4800}}'.format(message_number),
                    TEST_EMAIL_BASE64_FILENAME,
                    ' FLAGS ({}))'.format(message.get_flags())
                )
            )
        return ('OK', results)

    def login(self, user, password):
        return ('OK', ['{} authenticated (Success)'.format(user)])

    def logout(self):
        return ('BYE', ['LOGOUT Requested'])

    def search(self, charset, *criteria):
        """
        7.2.5.  SEARCH Response
        Contents:   zero or more numbers
        The SEARCH response occurs as a result of a SEARCH or UID SEARCH
        command.  The number(s) refer to those messages that match the
        search criteria.  For SEARCH, these are message sequence numbers;
        for UID SEARCH, these are unique identifiers.  Each number is
        delimited by a space.

        Example:    S: * SEARCH 2 3 6
        """
        results = [
            self.mailbox_selected.messages[0]
        ]

        message_sequences = []
        for result in results:
            message_sequences.append(
                force_text(
                    self.mailbox_selected.messages.index(result)
                )
            )

        return ('OK', ' '.join(message_sequences))

    def select(self, mailbox='INBOX', readonly=False):
        self.mailbox_selected = self.mailboxes[mailbox]

        return (
            'OK', [
                len(self.mailbox_selected.messages)
            ]
        )

    def store(self, message_set, command, flags):
        results = []

        for message_number in message_set.split():
            message = self.mailbox_selected.messages[int(message_number) - 1]

            if command == 'FLAGS':
                message.flags = flags.split()
            elif command == '+FLAGS':
                for flag in flags.split():
                    if flag not in message.flags:
                        message.flags.append(flag)
            elif command == '-FLAGS':
                for flag in flags.split():
                    if flag in message.flags:
                        message.flags.remove(flag)

            results.append(
                '{} (FLAGS ({}))'.format(message_number, message.get_flags())
            )

        return ('OK', results)
