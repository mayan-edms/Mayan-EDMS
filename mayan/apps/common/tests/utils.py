from contextlib import contextmanager
import sys


class NullFile(object):
    def write(self, string):
        """Writes here go nowhere"""


@contextmanager
def mute_stdout():
    stdout_old = sys.stdout
    sys.stdout = NullFile()
    yield
    sys.stdout = stdout_old
