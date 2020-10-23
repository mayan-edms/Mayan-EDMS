class UserPasswordViewTestMixin:
    def _request_test_user_password_set_view(self, password):
        return self.post(
            viewname='authentication:user_set_password', kwargs={
                'user_id': self.test_user.pk
            }, data={
                'new_password1': password, 'new_password2': password
            }
        )

    def _request_test_user_password_set_multiple_view(self, password):
        return self.post(
            viewname='authentication:user_multiple_set_password', data={
                'id_list': self.test_user.pk,
                'new_password1': password,
                'new_password2': password
            }
        )


class UserImpersonationViewTestMixin:
    def _impersonate_test_user(self):
        session = self.client.session
        session['_impersonate_id'] = self.test_user.pk
        session.save()

    def _request_impersonate_end_view(self):
        return self.get(
            follow=True, viewname='authentication:impersonate_end'
        )

    def _request_impersonate_start_view(self):
        return self.post(
            follow=True, viewname='authentication:impersonate_start', data={
                'user': self.test_user.pk
            }
        )


class UserLoginTestMixin:
    def _request_authenticated_view(self):
        return self.get(path=self.authenticated_url)

    def _request_password_reset_get_view(self):
        return self.get(
            viewname='authentication:password_reset_view', data={
                'email': self._test_case_superuser.email,
            }
        )

    def _request_password_reset_post_view(self):
        return self.post(
            viewname='authentication:password_reset_view', data={
                'email': self._test_case_superuser.email,
            }
        )
