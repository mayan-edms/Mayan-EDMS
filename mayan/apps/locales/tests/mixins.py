from .literals import TEST_USER_LOCALE_LANGUAGE, TEST_USER_LOCALE_TIMEZONE


class UserLocaleProfileViewMixin:
    def _request_test_current_user_locale_profile_detail_view(self):
        return self._request_test_user_locale_profile_detail_view(
            user=self._test_case_user
        )

    def _request_test_current_user_locale_profile_edit_view(
        self, follow=None
    ):
        return self._request_test_user_locale_profile_edit_view(
            user=self._test_case_user, follow=follow
        )

    def _request_test_superuser_locale_profile_detail_view(self):
        return self._request_test_user_locale_profile_detail_view(
            user=self.test_superuser
        )

    def _request_test_superuser_locale_profile_edit_view(self):
        return self._request_test_user_locale_profile_edit_view(
            user=self.test_superuser
        )

    def _request_test_user_locale_profile_detail_view(self, user=None):
        user = user or self.test_user

        return self.get(
            viewname='locales:user_locale_profile_detail', kwargs={
                'user_id': user.pk
            }
        )

    def _request_test_user_locale_profile_edit_view(
        self, follow=None, user=None
    ):
        user = user or self.test_user

        return self.post(
            viewname='locales:user_locale_profile_edit', kwargs={
                'user_id': user.pk
            }, data={
                'language': TEST_USER_LOCALE_LANGUAGE,
                'timezone': TEST_USER_LOCALE_TIMEZONE
            }, follow=follow
        )
