from __future__ import unicode_literals

from ..models import Key

from .literals import TEST_KEY_PRIVATE_DATA


class KeyAPIViewTestMixin(object):
    def _request_test_key_create_view(self):
        return self.post(
            viewname='rest_api:key-list', data={
                'key_data': TEST_KEY_PRIVATE_DATA
            }
        )

    def _request_test_key_delete_view(self):
        return self.delete(
            viewname='rest_api:key-detail', kwargs={
                'pk': self.test_key_private.pk
            }
        )

    def _request_test_key_detail_view(self):
        return self.get(
            viewname='rest_api:key-detail', kwargs={
                'pk': self.test_key_private.pk
            }
        )


class KeyTestMixin(object):
    def _create_test_key_private(self):
        self.test_key_private = Key.objects.create(
            key_data=TEST_KEY_PRIVATE_DATA
        )


class KeyViewTestMixin(object):
    def _request_test_key_download_view(self):
        return self.get(
            viewname='django_gpg:key_download', kwargs={
                'pk': self.test_key_private.pk
            }
        )

    def _request_test_key_upload_view(self):
        return self.post(
            viewname='django_gpg:key_upload', data={
                'key_data': TEST_KEY_PRIVATE_DATA
            }
        )
