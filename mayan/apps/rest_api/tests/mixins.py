class RESTAPIViewTestMixin:
    def _request_test_browser_api_view(self):
        return self.get(query={'format': 'api'}, viewname='rest_api:api_root')

    def _request_test_redoc_ui_view(self):
        return self.get(viewname='rest_api:schema-redoc')

    def _request_test_swagger_ui_view(self):
        return self.get(viewname='rest_api:schema-swagger-ui')

    def _request_test_swagger_no_ui_json_view(self):
        return self.get(
            kwargs={'format': '.json'}, viewname='rest_api:schema-json'
        )

    def _request_test_swagger_no_ui_yaml_view(self):
        return self.get(
            kwargs={'format': '.yaml'}, viewname='rest_api:schema-json'
        )
