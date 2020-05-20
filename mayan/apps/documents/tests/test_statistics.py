from mayan.apps.common.tests.base import BaseTestCase

from ..statistics import namespace


class DocumentStatisticsTestCase(BaseTestCase):
    def test_namespace(self):
        for statistic in namespace.statistics:
            try:
                statistic.execute()
            except Exception as exception:
                self.fail(
                    'Error executing: {};  {}'.format(statistic, exception)
                )
                raise
