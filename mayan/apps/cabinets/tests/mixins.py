from __future__ import unicode_literals

from ..models import Cabinet

from .literals import TEST_CABINET_LABEL


class CabinetTestMixin(object):
    def _create_test_cabinet(self):
        self.test_cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)
