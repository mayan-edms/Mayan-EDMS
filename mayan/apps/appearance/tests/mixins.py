from ..models import Theme

from .literals import TEST_THEME_LABEL, TEST_THEME_LABEL_EDITED


class ThemeTestMixin:
    def _create_test_theme(self):
        self.test_theme = Theme.objects.create(
            label=TEST_THEME_LABEL
        )

    def _edit_test_theme(self):
        self.test_theme.label = TEST_THEME_LABEL_EDITED
        self.test_theme.save()


class ThemeViewTestMixin:
    def _request_test_theme_create_view(self):
        pk_list = list(Theme.objects.values_list('pk', flat=True))

        response = self.post(
            viewname='appearance:theme_create', data={
                'label': TEST_THEME_LABEL,
            }
        )

        self.test_theme = Theme.objects.exclude(pk__in=pk_list).first()

        return response

    def _request_test_theme_delete_view(self):
        return self.post(
            viewname='appearance:theme_delete', kwargs={
                'theme_id': self.test_theme.pk
            }
        )

    def _request_test_theme_edit_view(self):
        return self.post(
            viewname='appearance:theme_edit', kwargs={
                'theme_id': self.test_theme.pk
            }, data={
                'label': TEST_THEME_LABEL_EDITED,
            }
        )

    def _request_test_theme_list_view(self):
        return self.get(viewname='appearance:theme_list')
