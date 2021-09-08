class DashboardViewTestMixin:
    def _request_test_dashboard_detail_view(self):
        return self.get(
            viewname='dashboards:dashboard_detail', kwargs={
                'dashboard_name': self.test_dashboard.name
            }
        )

    def _request_test_dashboard_list_view(self):
        return self.get(viewname='dashboards:dashboard_list')
