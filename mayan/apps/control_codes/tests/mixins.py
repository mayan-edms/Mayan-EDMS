from __future__ import unicode_literals

from ..models import ControlSheet

from .literals import TEST_CONTROL_SHEET_LABEL


class ControlSheetAPIViewTestMixin(object):
    def _request_test_tag_create_api_view(self):
        return self.post(
            viewname='rest_api:tag-list', data={
                'label': TEST_CONTROL_SHEET_LABEL, 'color': TEST_CONTROL_SHEET_COLOR
            }
        )


    def _request_test_control_sheet_delete_api_view(self):
        return self.delete(
            viewname='rest_api:control_sheet-detail', kwargs={'pk': self.test_control_sheet.pk}
        )

    def _request_control_sheet_edit_view(self, extra_data=None, verb='patch'):
        data = {
            'label': TEST_CONTROL_SHEET_LABEL_EDITED,
        }

        if extra_data:
            data.update(extra_data)

        return getattr(self, verb)(
            viewname='rest_api:control_sheet-detail', kwargs={
                'control_sheet_id': self.test_control_sheet.pk
            }, data=data
        )


class ControlSheetTestMixin(object):
    def _create_test_control_sheet(self):
        self.test_control_sheet = ControlSheet.objects.create(
            label=TEST_CONTROL_SHEET_LABEL
        )


class ControlSheetViewTestMixin(object):
    def _request_test_control_sheet_create_view(self):
        return self.post(
            viewname='control_codes:control_sheet_create', data={
                'label': TEST_CONTROL_SHEET_LABEL
            }
        )

    def _request_test_control_sheet_delete_view(self):
        return self.post(
            viewname='control_codes:control_sheet_delete',
            kwargs={'control_sheet_id': self.test_control_sheet.pk}
        )

    def _request_test_control_sheet_delete_multiple_view(self):
        return self.post(
            viewname='control_codes:control_sheet_multiple_delete',
            data={'id_list': self.test_control_sheet.pk},
        )

    def _request_test_control_sheet_edit_view(self):
        return self.post(
            viewname='control_codes:control_sheet_edit',
            kwargs={'control_sheet_id': self.test_control_sheet.pk}, data={
                'label': TEST_CONTROL_SHEET_LABEL_EDITED,
            }
        )

    def _request_test_control_sheet_list_view(self):
        return self.get(viewname='control_sheets:control_sheet_list')
