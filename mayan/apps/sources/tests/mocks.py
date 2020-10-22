from django.utils.encoding import force_bytes, force_text

from .literals import TEST_EMAIL_BASE64_FILENAME


class MockIMAPMessage(object):
    def __init__(self, uid):
        self.flags = []
        self.mailbox = None
        self.uid = uid

    def flags_add(self, flags_string):
        for flag in flags_string.split():
            if flag in self.flags:
                self.flags.remove(flag)

    def flags_remove(self, flags_string):
        for flag in flags_string.split():
            if flag not in self.flags:
                self.flags.append(flag)

    def flags_set(self, flags_string):
        self.flags = flags_string.split()

    def delete(self):
        self.mailbox.messages.pop(self.uid)

    def get_flags(self):
        return ' '.join(self.flags)

    def get_number(self):
        return list(self.mailbox.messages.values()).index(self)


class MockIMAPMailbox(object):
    messages = {}

    def __init__(self, name='INBOX'):
        self.name = name

    def get_message_by_number(self, message_number):
        return list(self.messages.values())[message_number - 1]

    def get_message_by_uid(self, uid):
        return self.messages[uid]

    def get_message_count(self):
        return len(self.messages)

    def get_messages(self):
        return list(self.messages.values())

    def messages_add(self, uid):
        self.messages[uid] = MockIMAPMessage(uid=uid)
        self.messages[uid].mailbox = self


class MockIMAPServer(object):
    def __init__(self):
        self.mailboxes = {
            'INBOX': MockIMAPMailbox(name='INBOX')
        }
        self.mailboxes['INBOX'].messages_add(uid='999')
        self.mailbox_selected = None

    def _fetch(self, messages):
        flag = '\\Seen'
        flag_modified = []
        message_numbers = []
        results = []
        uids = []

        for message in messages:
            if flag not in message.flags:
                message.flags_add(flag)
                flag_modified.append(message)

            message_number = message.get_number()
            message_numbers.append(force_text(s=message_number))
            uid = message.uid
            uids.append(uid)
            body = TEST_EMAIL_BASE64_FILENAME

            results.append(
                (
                    '{} (UID {} RFC822 {{{}}}'.format(message_number, uid, len(body)),
                    body,
                )
            )

        results.append(
            ' FLAGS ({}))'.format(flag),
        )
        results.append(
            '{} (UID {} FLAGS ({}))'.format(
                ' '.join(message_numbers), ' '.join(uids), flag
            )
        )
        return results

    def close(self):
        return ('OK', ['Returned to authenticated state. (Success)'])

    def expunge(self):
        result = []

        for message in self.mailbox_selected.get_messages():
            if '\\Deleted' in message.flags:
                result.append(
                    force_text(s=message.get_number())
                )
                message.delete()

        return ('OK', ' '.join(result))

    def fetch(self, message_set, message_parts):
        messages = []

        for message_number in message_set.split():
            messages.append(
                self.mailbox_selected.get_message_by_number(
                    message_number=int(message_number)
                )
            )

        return ('OK', self._fetch(messages=messages))

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
        for message in results:
            message_sequences.append(force_text(s=message.get_number()))

        return ('OK', ' '.join(message_sequences))

    def select(self, mailbox='INBOX', readonly=False):
        self.mailbox_selected = self.mailboxes[mailbox]

        return (
            'OK', [
                self.mailbox_selected.get_message_count()
            ]
        )

    def store(self, message_set, command, flags):
        results = []

        for message_number in message_set.split():
            message = self.mailbox_selected.messages[int(message_number) - 1]

            if command == 'FLAGS':
                message.flags_set(flags_string=flags)
            elif command == '+FLAGS':
                message.flags_add(flags_string=flags)
            elif command == '-FLAGS':
                message.flags_remove(flags_string=flags)

            results.append(
                '{} (FLAGS ({}))'.format(message_number, message.get_flags())
            )

        return ('OK', results)

    def uid(self, command, *args):
        if command == 'FETCH':
            uid = args[0]
            messages = [self.mailbox_selected.get_message_by_uid(uid=uid)]
            return ('OK', self._fetch(messages=messages))
        elif command == 'STORE':
            results = []
            uid = args[0]
            subcommand = args[1]
            flags = args[2]
            message = self.mailbox_selected.get_message_by_uid(uid=uid)

            if subcommand == 'FLAGS':
                message.flags_set(flags_string=flags)
            elif subcommand == '+FLAGS':
                message.flags_add(flags_string=flags)
            elif subcommand == '-FLAGS':
                message.flags_remove(flags_string=flags)

            results.append(
                '{} (FLAGS ({}))'.format(uid, message.get_flags())
            )
            return ('OK', results)
        elif command == 'SEARCH':
            message_sequences = [
                self.mailbox_selected.get_message_by_number(
                    message_number=1
                ).uid
            ]

            return ('OK', [' '.join(message_sequences)])


class MockPOP3Mailbox(object):
    """RFC 1725"""
    messages = {
        1: [TEST_EMAIL_BASE64_FILENAME]
    }

    def dele(self, which):
        return

    def getwelcome(self):
        return force_bytes(
            '+OK server ready for requests from 127.0.0.0 xxxxxxxxxxxxxxxxx'
        )

    def list(self, which=None):
        # (b'+OK 7 messages (304882 bytes)',
        # [b'1 4800',
        #  b'2 16995',
        #  b'3 12580',
        #  b'4 196497',
        #  b'5 48900',
        #  b'6 12555',
        #  b'7 12555'],
        #  63)

        message_list = []
        message_number = 1
        messages_total_size = 0

        for key, value in self.messages.items():
            message_size = 0
            for line in value:
                message_size = message_size + len(line)

            messages_total_size = messages_total_size + message_size
            message_list.append(
                force_bytes('{} {}'.format(message_number, message_size))
            )

            message_number = message_number + 1

        # Sum the line sizes in bytes plus 2 (CR+LF)
        result_size = sum(
            [len(message_entry) + 2 for message_entry in message_list]
        )

        return (
            force_bytes(
                '+OK {} messages ({} bytes)'.format(
                    len(self.messages), messages_total_size
                )
            ), message_list, result_size
        )

    def user(self, user):
        return force_bytes('+OK send PASS')

    def pass_(self, pswd):
        return force_bytes('+OK Welcome.')

    def quit(self):
        return

    def retr(self, which):
        return (None, self.messages[which], None)


class MockStagingFolder(object):
    """Mock of a StagingFolder model"""
