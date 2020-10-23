class StatisticsViewTestMixin:
    def _request_test_statistic_detail_view(self):
        return self.get(
            viewname='statistics:statistic_detail', kwargs={
                'slug': self.statistic.slug
            }
        )

    def _request_test_namespace_list_view(self):
        return self.get(viewname='statistics:namespace_list')
