from __future__ import unicode_literals

from ..models import SmartLink, SmartLinkCondition

from .literals import (
    TEST_SMART_LINK_CONDITION_FOREIGN_DOCUMENT_DATA,
    TEST_SMART_LINK_CONDITION_EXPRESSION,
    TEST_SMART_LINK_CONDITION_OPERATOR, TEST_SMART_LINK_DYNAMIC_LABEL,
    TEST_SMART_LINK_LABEL
)


class SmartLinkTestMixin(object):
    def _create_test_smart_link(self, add_test_document_type=False):
        self.test_smart_link = SmartLink.objects.create(
            label=TEST_SMART_LINK_LABEL,
            dynamic_label=TEST_SMART_LINK_DYNAMIC_LABEL
        )
        if add_test_document_type:
            self.test_smart_link.document_types.add(self.test_document_type)

    def _create_test_smart_link_condition(self):
        self.test_smart_link_condition = SmartLinkCondition.objects.create(
            smart_link=self.test_smart_link,
            foreign_document_data=TEST_SMART_LINK_CONDITION_FOREIGN_DOCUMENT_DATA,
            expression=TEST_SMART_LINK_CONDITION_EXPRESSION,
            operator=TEST_SMART_LINK_CONDITION_OPERATOR
        )
