from __future__ import unicode_literals

from ..models import ControlSheet

from .control_codes import ControlCodeTest
from .literals import (
    TEST_CONTROL_SHEET_CODE_ARGUMENTS,
    TEST_CONTROL_SHEET_CODE_ARGUMENTS_EDITED, TEST_CONTROL_SHEET_LABEL,
    TEST_CONTROL_SHEET_LABEL_EDITED
)


class ControlSheetAPIViewTestMixin(object):
    def _request_test_control_sheet_create_api_view(self):
        return self.post(
            viewname='rest_api:control_sheet-list', data={
                'label': TEST_CONTROL_SHEET_LABEL,
            }
        )

    def _request_test_control_sheet_delete_api_view(self):
        return self.delete(
            viewname='rest_api:control_sheet-detail', kwargs={
                'control_sheet_id': self.test_control_sheet.pk
            }
        )

    def _request_test_control_sheet_edit_api_view(self, extra_data=None, verb='patch'):
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


class ControlSheetCodeTestMixin(object):
    _test_control_code_class = ControlCodeTest

    def _create_test_control_sheet_code(self):
        self.test_control_sheet_code = self.test_control_sheet.codes.create(
            control_sheet=self.test_control_sheet,
            name=self._test_control_code_class.name,
            arguments=TEST_CONTROL_SHEET_CODE_ARGUMENTS
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
            viewname='control_codes:control_sheet_delete', kwargs={
                'control_sheet_id': self.test_control_sheet.pk
            }
        )

    def _request_test_control_sheet_delete_multiple_view(self):
        return self.post(
            viewname='control_codes:control_sheet_multiple_delete', data={
                'id_list': self.test_control_sheet.pk
            },
        )

    def _request_test_control_sheet_edit_view(self):
        return self.post(
            viewname='control_codes:control_sheet_edit', kwargs={
                'control_sheet_id': self.test_control_sheet.pk
            }, data={
                'label': TEST_CONTROL_SHEET_LABEL_EDITED,
            }
        )

    def _request_test_control_sheet_list_view(self):
        return self.get(viewname='control_codes:control_sheet_list')

    def _request_test_control_sheet_preview_view(self):
        return self.get(
            viewname='control_codes:control_sheet_preview', kwargs={
                'control_sheet_id': self.test_control_sheet.pk
            }
        )

    def _request_test_control_sheet_print_view(self):
        return self.get(
            viewname='control_codes:control_sheet_print', kwargs={
                'control_sheet_id': self.test_control_sheet.pk
            }
        )


class ControlSheetCodeViewTestMixin(object):
    def _request_test_control_sheet_code_select_get_view(self):
        return self.get(
            viewname='control_codes:control_sheet_code_select', kwargs={
                'control_sheet_id': self.test_control_sheet.pk,
            }
        )

    def _request_test_control_sheet_code_select_post_view(self):
        return self.post(
            viewname='control_codes:control_sheet_code_select', kwargs={
                'control_sheet_id': self.test_control_sheet.pk,
            }, data={'control_code_class_name': self._test_control_code_class.name}
        )

    def _request_test_control_sheet_code_create_view(self):
        return self.post(
            viewname='control_codes:control_sheet_code_create', kwargs={
                'control_sheet_id': self.test_control_sheet.pk,
                'control_code_class_name': self._test_control_code_class.name
            }
        )

    def _request_test_control_sheet_code_delete_view(self):
        return self.post(
            viewname='control_codes:control_sheet_code_delete',
            kwargs={
                'control_sheet_id': self.test_control_sheet_code.control_sheet.pk,
                'control_sheet_code_id': self.test_control_sheet_code.pk
            }
        )

    def _request_test_control_sheet_code_edit_view(self):
        return self.post(
            viewname='control_codes:control_sheet_code_edit', kwargs={
                'control_sheet_id': self.test_control_sheet_code.control_sheet.pk,
                'control_sheet_code_id': self.test_control_sheet_code.pk
            }, data={
                'arguments': TEST_CONTROL_SHEET_CODE_ARGUMENTS_EDITED,
            }
        )

    def _request_test_control_sheet_code_list_view(self):
        return self.get(
            viewname='control_codes:control_sheet_code_list', kwargs={
                'control_sheet_id': self.test_control_sheet.pk
            }
        )
