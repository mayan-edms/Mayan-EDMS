from __future__ import unicode_literals


class UserPasswordViewTestMixin(object):
    def _request_test_user_password_set_view(self, password):
        return self.post(
            viewname='authentication:user_set_password',
            kwargs={'pk': self.test_user.pk},
            data={
                'new_password1': password, 'new_password2': password
            }
        )

    def _request_test_user_password_set_multiple_view(self, password):
        return self.post(
            viewname='authentication:user_multiple_set_password',
            data={
                'id_list': self.test_user.pk,
                'new_password1': password,
                'new_password2': password
            }
        )
