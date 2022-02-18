from django.contrib.auth import get_user_model

from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.metadata.permissions import permission_document_metadata_edit
from mayan.apps.metadata.tests.mixins import MetadataTypeTestMixin
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_user_created, event_user_edited
from ..permissions import (
    permission_group_edit, permission_user_create, permission_user_delete,
    permission_user_edit, permission_user_view
)

from .mixins import (
    CurrentUserViewTestMixin, GroupTestMixin, UserGroupViewTestMixin,
    UserViewTestMixin
)


class CurrentUserViewTestCase(CurrentUserViewTestMixin, GenericViewTestCase):
    def test_current_user_detail_view_no_permission(self):
        self._clear_events()

        response = self._request_current_user_details_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_current_user_edit_get_view_no_permission(self):
        self._clear_events()

        response = self._request_current_user_edit_view()
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(
            response=response, status_code=200, text='Is active'
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_current_user_edit_get_view_with_access(self):
        self.grant_access(
            obj=self._test_case_user, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_current_user_edit_view()
        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response=response, status_code=200, text='Is active'
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_current_user_edit_post_view_no_permission(self):
        test_first_name = self._test_case_user.first_name
        test_username = self._test_case_user.username

        self._clear_events()

        response = self._request_current_user_post_view()
        self.assertEqual(response.status_code, 302)

        self._test_case_user.refresh_from_db()

        self.assertEqual(self._test_case_user.username, test_username)
        self.assertNotEqual(self._test_case_user.first_name, test_first_name)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_case_user)
        self.assertEqual(events[0].verb, event_user_edited.id)

    def test_current_user_edit_post_view_with_access(self):
        self.grant_access(
            obj=self._test_case_user, permission=permission_user_edit
        )

        test_first_name = self._test_case_user.first_name
        test_username = self._test_case_user.username

        self._clear_events()

        response = self._request_current_user_post_view()
        self.assertEqual(response.status_code, 302)

        self._test_case_user.refresh_from_db()

        self.assertNotEqual(self._test_case_user.username, test_username)
        self.assertNotEqual(self._test_case_user.first_name, test_first_name)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_case_user)
        self.assertEqual(events[0].verb, event_user_edited.id)


class CurrentUserSuperUserViewTestCase(
    CurrentUserViewTestMixin, GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._test_case_user.is_superuser = True
        self._test_case_user.save()

    def test_current_user_detail_view_no_permission(self):
        self._clear_events()

        response = self._request_current_user_details_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_current_user_edit_get_view_no_permission(self):
        self._clear_events()

        response = self._request_current_user_edit_view()
        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response=response, status_code=200, text='Is active'
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_current_user_edit_post_view_no_permission(self):
        test_first_name = self._test_case_user.first_name
        test_username = self._test_case_user.username

        self._clear_events()

        response = self._request_current_user_post_view()
        self.assertEqual(response.status_code, 302)

        self._test_case_user.refresh_from_db()

        self.assertNotEqual(self._test_case_user.username, test_username)
        self.assertNotEqual(self._test_case_user.first_name, test_first_name)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_case_user)
        self.assertEqual(events[0].verb, event_user_edited.id)


class SuperUserViewTestCase(
    UserViewTestMixin, GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_superuser()

    def test_superuser_delete_view_with_access(self):
        superuser_count = get_user_model().objects.filter(
            is_superuser=True
        ).count()
        self.grant_access(
            obj=self.test_superuser, permission=permission_user_delete
        )

        self._clear_events()

        response = self._request_test_superuser_delete_view()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            get_user_model().objects.filter(is_superuser=True).count(),
            superuser_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_superuser_detail_view_with_access(self):
        self.grant_access(
            obj=self.test_superuser, permission=permission_user_view
        )

        self._clear_events()

        response = self._request_test_superuser_detail_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_superuser_normal_user_detail_view_with_access(self):
        self.grant_access(
            obj=self.test_superuser, permission=permission_user_view
        )

        self.test_user = self.test_superuser

        self._clear_events()

        response = self._request_test_user_detail_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class UserViewTestCase(UserViewTestMixin, GenericViewTestCase):
    def test_user_create_view_no_permission(self):
        user_count = get_user_model().objects.count()

        self._clear_events()

        response = self._request_test_user_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(get_user_model().objects.count(), user_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_create_view_with_permission(self):
        self.grant_permission(permission=permission_user_create)

        user_count = get_user_model().objects.count()

        self._clear_events()

        response = self._request_test_user_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(get_user_model().objects.count(), user_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_user)
        self.assertEqual(events[0].verb, event_user_created.id)

    def test_user_delete_view_no_permission(self):
        self._create_test_user()

        user_count = get_user_model().objects.count()

        self._clear_events()

        response = self._request_test_user_delete_single_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(get_user_model().objects.count(), user_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_delete_view_with_access(self):
        self._create_test_user()

        user_count = get_user_model().objects.count()

        self.grant_access(
            obj=self.test_user, permission=permission_user_delete
        )

        self._clear_events()

        response = self._request_test_user_delete_single_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(get_user_model().objects.count(), user_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_delete_multiple_view_no_permission(self):
        self._create_test_user()

        user_count = get_user_model().objects.count()

        self._clear_events()

        response = self._request_test_user_delete_multiple_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(get_user_model().objects.count(), user_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_delete_multiple_view_with_access(self):
        self._create_test_user()

        user_count = get_user_model().objects.count()

        self.grant_access(
            obj=self.test_user, permission=permission_user_delete
        )

        self._clear_events()

        response = self._request_test_user_delete_multiple_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(get_user_model().objects.count(), user_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_edit_view_no_permission(self):
        self._create_test_user()

        username = self.test_user.username

        self._clear_events()

        response = self._request_test_user_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.username, username)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_edit_view_with_access(self):
        self._create_test_user()

        username = self.test_user.username

        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_test_user_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_user.refresh_from_db()
        self.assertNotEqual(self.test_user.username, username)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_user)
        self.assertEqual(events[0].verb, event_user_edited.id)

    def test_user_list_view_no_permission(self):
        self._create_test_user()

        self._clear_events()

        response = self._request_test_user_list_view()
        self.assertNotContains(
            response=response, text=self.test_user.username, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_list_view_with_permission(self):
        self._create_test_user()

        self.grant_access(
            obj=self.test_user, permission=permission_user_view
        )

        self._clear_events()

        response = self._request_test_user_list_view()
        self.assertContains(
            response=response, text=self.test_user.username, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class UserGroupViewTestCase(
    GroupTestMixin, UserGroupViewTestMixin, GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_group()
        self._create_test_user()

    def test_user_group_add_remove_get_view_no_permission(self):
        self.test_group.user_set.add(self.test_user)

        self._clear_events()

        response = self._request_test_user_group_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_group),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_user),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_group_add_remove_get_view_with_group_access(self):
        self.test_group.user_set.add(self.test_user)

        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_user_group_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_group),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_user),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_group_add_remove_get_view_with_user_access(self):
        self.test_group.user_set.add(self.test_user)

        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_test_user_group_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_group),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self.test_user),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_group_add_remove_get_view_with_full_access(self):
        self.test_group.user_set.add(self.test_user)

        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )
        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_test_user_group_add_remove_get_view()
        self.assertContains(
            response=response, text=str(self.test_group),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self.test_user),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_group_add_view_no_permission(self):
        self._clear_events()

        response = self._request_test_user_group_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_group not in self.test_user.groups.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_group_add_view_with_group_access(self):
        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_user_group_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_group not in self.test_user.groups.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_group_add_view_with_user_access(self):
        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_test_user_group_add_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self.test_group not in self.test_user.groups.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_group_add_view_with_full_access(self):
        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )
        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_test_user_group_add_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.test_group in self.test_user.groups.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_group)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_user)
        self.assertEqual(events[0].verb, event_user_edited.id)

    def test_user_group_remove_view_no_permission(self):
        self.test_group.user_set.add(self.test_user)

        self._clear_events()

        response = self._request_test_user_group_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_group in self.test_user.groups.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_group_remove_view_with_group_access(self):
        self.test_group.user_set.add(self.test_user)

        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_user_group_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_group in self.test_user.groups.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_group_remove_view_with_user_access(self):
        self.test_group.user_set.add(self.test_user)

        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_test_user_group_remove_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self.test_group in self.test_user.groups.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_group_remove_view_with_full_access(self):
        self.test_group.user_set.add(self.test_user)

        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )
        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_test_user_group_remove_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.test_group not in self.test_user.groups.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_group)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_user)
        self.assertEqual(events[0].verb, event_user_edited.id)


class UserOptionsViewTestCase(
    UserViewTestMixin, GenericViewTestCase
):
    def test_user_options_view_no_permission(self):
        self._create_test_user()

        self._clear_events()

        response = self._request_test_user_options_view()
        self.assertEqual(response.status_code, 404)

        self.test_user.user_options.refresh_from_db()
        self.assertFalse(self.test_user.user_options.block_password_change)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_options_view_with_access(self):
        self._create_test_user()

        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_test_user_options_view()
        self.assertEqual(response.status_code, 302)

        self.test_user.user_options.refresh_from_db()
        self.assertTrue(self.test_user.user_options.block_password_change)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_user)
        self.assertEqual(events[0].verb, event_user_edited.id)


class MetadataLookupIntegrationTestCase(
    MetadataTypeTestMixin, GenericDocumentViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_metadata_type()
        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type
        )

    def test_user_list_lookup_render(self):
        self.test_metadata_type.lookup = '{{ users }}'
        self.test_metadata_type.save()
        self.test_document.metadata.create(
            metadata_type=self.test_metadata_type
        )

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        self._clear_events()

        response = self.get(
            viewname='metadata:metadata_edit', kwargs={
                'document_id': self.test_document.pk
            }
        )
        self.assertContains(
            response=response, text='<option value="{}">{}</option>'.format(
                self._test_case_user.username, self._test_case_user.username
            ), status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
