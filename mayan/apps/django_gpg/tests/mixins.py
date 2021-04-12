from django.db.models import Q

from ..models import Key

from .literals import TEST_KEY_PRIVATE_DATA, TEST_KEY_PUBLIC_FILE_PATH


class KeyAPIViewTestMixin:
    def _request_test_key_create_api_view(self):
        pk_list = list(Key.objects.values_list('pk', flat=True))

        response = self.post(
            viewname='rest_api:key-list', data={
                'key_data': TEST_KEY_PRIVATE_DATA
            }
        )

        try:
            self.test_key_private = Key.objects.get(
                ~Q(pk__in=pk_list)
            )
        except Key.DoesNotExist:
            self.test_key_private = None

        return response

    def _request_test_key_delete_api_view(self):
        return self.delete(
            viewname='rest_api:key-detail', kwargs={
                'key_id': self.test_key_private.pk
            }
        )

    def _request_test_key_detail_api_view(self):
        return self.get(
            viewname='rest_api:key-detail', kwargs={
                'key_id': self.test_key_private.pk
            }
        )


class KeyTestMixin:
    def _create_test_key_private(self):
        self.test_key_private = Key.objects.create(
            key_data=TEST_KEY_PRIVATE_DATA
        )

    def _create_test_key_public(self):
        with open(file=TEST_KEY_PUBLIC_FILE_PATH, mode='rb') as file_object:
            self.test_key_public = Key.objects.create(
                key_data=file_object.read()
            )


class KeyViewTestMixin:
    def _request_test_key_delete_view(self):
        return self.post(
            viewname='django_gpg:key_delete', kwargs={
                'key_id': self.test_key_private.pk
            }
        )

    def _request_test_key_download_view(self):
        return self.get(
            viewname='django_gpg:key_download', kwargs={
                'key_id': self.test_key_private.pk
            }
        )

    def _request_test_key_upload_view(self):
        pk_list = list(Key.objects.values_list('pk', flat=True))

        response = self.post(
            viewname='django_gpg:key_upload', data={
                'key_data': TEST_KEY_PRIVATE_DATA
            }
        )

        try:
            self.test_key_private = Key.objects.get(
                ~Q(pk__in=pk_list)
            )
        except Key.DoesNotExist:
            self.test_key_private = None

        return response
