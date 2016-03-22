from __future__ import unicode_literals

from django.test import TestCase

from ..models import Key

from .literals import TEST_KEY_DATA, TEST_KEY_FINGERPRINT, TEST_KEY_ID


class KeyTestCase(TestCase):
    def test_key_instance_creation(self):
        # Creating a Key instance is analogous to importing a key
        key = Key.objects.create(key_data=TEST_KEY_DATA)

        self.assertEqual(key.key_id, TEST_KEY_ID)
        self.assertEqual(key.fingerprint, TEST_KEY_FINGERPRINT)
