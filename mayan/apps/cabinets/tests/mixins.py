from __future__ import unicode_literals

from ..models import Cabinet

from .literals import TEST_CABINET_LABEL, TEST_CABINET_CHILD_LABEL


class CabinetTestMixin(object):
    def _create_test_cabinet(self):
        self.test_cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

    def _create_test_cabinet_child(self):
        self.test_cabinet_child = Cabinet.objects.create(
            label=TEST_CABINET_CHILD_LABEL, parent=self.test_cabinet
        )


class CabinetViewTestMixin(object):
    def _request_test_cabinet_child_create_view(self):
        return self.post(
            viewname='cabinets:cabinet_child_add', kwargs={
                'pk': self.test_cabinet.pk
            }, data={'label': TEST_CABINET_CHILD_LABEL}
        )

    def _request_test_cabinet_child_delete_view(self):
        return self.post(
            viewname='cabinets:cabinet_delete', kwargs={
                'pk': self.test_cabinet_child.pk
            }
        )
