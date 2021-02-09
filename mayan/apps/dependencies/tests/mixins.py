from .literals import (
    TEST_DEPENDENCY_GROUP_NAME, TEST_DEPENDENCY_GROUP_ENTRY_NAME
)


class CheckVersionViewTestMixin:
    def _request_check_version_view(self):
        return self.get(viewname='dependencies:check_version_view')


class DependencyGroupEntryDetailViewTestMixin:
    def request_test_dependency_group_entry_detail_view(self):
        return self.get(
            viewname='dependencies:dependency_group_entry_detail', kwargs={
                'dependency_group_name': TEST_DEPENDENCY_GROUP_NAME,
                'dependency_group_entry_name': TEST_DEPENDENCY_GROUP_ENTRY_NAME
            }
        )
