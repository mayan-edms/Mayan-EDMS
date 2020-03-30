from ..models import SmartLink, SmartLinkCondition

from .literals import (
    TEST_SMART_LINK_CONDITION_FOREIGN_DOCUMENT_DATA,
    TEST_SMART_LINK_CONDITION_EXPRESSION,
    TEST_SMART_LINK_CONDITION_EXPRESSION_EDITED,
    TEST_SMART_LINK_CONDITION_INCLUSION, TEST_SMART_LINK_CONDITION_OPERATOR,
    TEST_SMART_LINK_DYNAMIC_LABEL, TEST_SMART_LINK_LABEL,
    TEST_SMART_LINK_LABEL_EDITED
)


class SmartLinkConditionViewTestMixin(object):
    def _request_test_smart_link_condition_create_view(self):
        return self.post(
            viewname='linking:smart_link_condition_create', kwargs={
                'smart_link_id': self.test_smart_link.pk
            }, data={
                'inclusion': TEST_SMART_LINK_CONDITION_INCLUSION,
                'foreign_document_data': TEST_SMART_LINK_CONDITION_FOREIGN_DOCUMENT_DATA,
                'expression': TEST_SMART_LINK_CONDITION_EXPRESSION,
                'operator': TEST_SMART_LINK_CONDITION_OPERATOR
            }
        )

    def _request_test_smart_link_condition_delete_view(self):
        return self.post(
            viewname='linking:smart_link_condition_delete', kwargs={
                'smart_link_condition_id': self.test_smart_link_condition.pk
            }
        )

    def _request_test_smart_link_condition_edit_view(self):
        return self.post(
            viewname='linking:smart_link_condition_edit', kwargs={
                'smart_link_condition_id': self.test_smart_link_condition.pk
            }, data={
                'inclusion': TEST_SMART_LINK_CONDITION_INCLUSION,
                'foreign_document_data': TEST_SMART_LINK_CONDITION_FOREIGN_DOCUMENT_DATA,
                'expression': TEST_SMART_LINK_CONDITION_EXPRESSION_EDITED,
                'operator': TEST_SMART_LINK_CONDITION_OPERATOR
            }
        )

    def _request_test_smart_link_condition_list_view(self):
        return self.get(
            viewname='linking:smart_link_condition_list', kwargs={
                'smart_link_id': self.test_smart_link.pk
            }
        )


class SmartLinkDocumentViewTestMixin(object):
    def _request_test_smart_link_document_instances_view(self):
        return self.get(
            viewname='linking:smart_link_instances_for_document', kwargs={
                'document_id': self.test_document.pk
            }
        )


class SmartLinkTestMixin(object):
    def _create_test_smart_link(self, add_test_document_type=False):
        self.test_smart_link = SmartLink.objects.create(
            label=TEST_SMART_LINK_LABEL,
            dynamic_label=TEST_SMART_LINK_DYNAMIC_LABEL
        )
        if add_test_document_type:
            self.test_smart_link.document_types.add(self.test_document_type)

    def _create_test_smart_links(self, add_test_document_type=False):
        self.test_smart_links = []
        self.test_smart_links.append(
            SmartLink.objects.create(
                label=TEST_SMART_LINK_LABEL,
                dynamic_label=TEST_SMART_LINK_DYNAMIC_LABEL
            )
        )
        self.test_smart_links.append(
            SmartLink.objects.create(
                label=TEST_SMART_LINK_LABEL,
                dynamic_label=TEST_SMART_LINK_DYNAMIC_LABEL
            )
        )
        if add_test_document_type:
            self.test_smart_links[0].document_types.add(
                self.test_document_type
            )
            self.test_smart_links[1].document_types.add(
                self.test_document_type
            )

    def _create_test_smart_link_condition(self):
        self.test_smart_link_condition = SmartLinkCondition.objects.create(
            smart_link=self.test_smart_link,
            foreign_document_data=TEST_SMART_LINK_CONDITION_FOREIGN_DOCUMENT_DATA,
            expression=TEST_SMART_LINK_CONDITION_EXPRESSION,
            operator=TEST_SMART_LINK_CONDITION_OPERATOR
        )


class SmartLinkViewTestMixin(object):
    def _request_test_smart_link_create_view(self):
        # Typecast to list to force queryset evaluation
        values = list(SmartLink.objects.values_list('pk', flat=True))

        response = self.post(
            viewname='linking:smart_link_create', data={
                'label': TEST_SMART_LINK_LABEL
            }
        )

        self.test_smart_link = SmartLink.objects.exclude(pk__in=values).first()

        return response

    def _request_test_smart_link_delete_view(self):
        return self.post(
            viewname='linking:smart_link_delete', kwargs={
                'smart_link_id': self.test_smart_link.pk
            }
        )

    def _request_test_smart_link_edit_view(self):
        return self.post(
            viewname='linking:smart_link_edit', kwargs={
                'smart_link_id': self.test_smart_link.pk
            }, data={
                'label': TEST_SMART_LINK_LABEL_EDITED
            }
        )
