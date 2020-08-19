from mayan.apps.common.settings import setting_home_view


class AutoAdminViewMixing:
    def _request_home_view(self):
        return self.get(viewname=setting_home_view.value, follow=True)
