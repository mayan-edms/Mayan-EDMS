import json

from ..models import Quota

from .literals import (
    TEST_QUOTA_DATA, TEST_QUOTA_DOTTED_PATH, TEST_QUOTA_WITH_MIXINS_DOTTED_PATH,
    TEST_QUOTA_TEST_LIMIT_EDITED
)


class QuotaTestMixin:
    def _create_test_quota(self):
        self.test_quota = Quota.objects.create(
            backend_data=json.dumps(obj=TEST_QUOTA_DATA),
            backend_path=TEST_QUOTA_DOTTED_PATH
        )

    def _create_test_quota_with_mixins(self):
        self.test_quota = Quota.objects.create(
            backend_data=json.dumps(obj=TEST_QUOTA_DATA),
            backend_path=TEST_QUOTA_WITH_MIXINS_DOTTED_PATH
        )


class QuotaViewTestMixin:
    def _request_test_quota_backend_selection_get_view(self):
        return self.get(viewname='quotas:quota_backend_selection')

    def _request_test_quota_create_get_view(self):
        values = list(Quota.objects.values_list('pk', flat=True))

        response = self.get(
            viewname='quotas:quota_create', kwargs={
                'class_path': TEST_QUOTA_DOTTED_PATH
            }
        )

        # Get the instance created ignoring existing ones.
        self.test_quota = Quota.objects.exclude(pk__in=values).first()

        return response

    def _request_test_quota_with_mixins_create_get_view(self):
        values = list(Quota.objects.values_list('pk', flat=True))

        response = self.get(
            viewname='quotas:quota_create', kwargs={
                'class_path': TEST_QUOTA_WITH_MIXINS_DOTTED_PATH
            }
        )

        # Get the instance created ignoring existing ones.
        self.test_quota = Quota.objects.exclude(pk__in=values).first()

        return response

    def _request_test_quota_create_post_view(self):
        values = list(Quota.objects.values_list('pk', flat=True))

        response = self.post(
            viewname='quotas:quota_create', kwargs={
                'class_path': TEST_QUOTA_DOTTED_PATH
            }, data=TEST_QUOTA_DATA
        )

        # Get the instance created ignoring existing ones.
        self.test_quota = Quota.objects.exclude(pk__in=values).first()

        return response

    def _request_test_quota_delete_view(self):
        return self.post(
            viewname='quotas:quota_delete', kwargs={
                'quota_id': self.test_quota.pk,
            }
        )

    def _request_test_quota_edit_view(self):
        return self.post(
            viewname='quotas:quota_edit', kwargs={
                'quota_id': self.test_quota.pk
            }, data={
                'test_limit': TEST_QUOTA_TEST_LIMIT_EDITED,
            }
        )

    def _request_test_quota_list_view(self):
        return self.get(viewname='quotas:quota_list')
