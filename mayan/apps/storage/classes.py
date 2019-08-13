from __future__ import unicode_literals


class FakeStorageSubclass(object):
    """
    Placeholder class to allow serializing the real storage subclass to
    support migrations.
    """
    def __eq__(self, other):
        return True
