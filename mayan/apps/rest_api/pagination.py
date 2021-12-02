from rest_framework import pagination

from .literals import DEFAULT_PAGE_SIZE_QUERY_PARAMETER
from .settings import setting_maximum_page_size, setting_page_size


class MayanPageNumberPagination(pagination.PageNumberPagination):
    max_page_size = setting_maximum_page_size.value
    page_size = setting_page_size.value
    page_size_query_param = DEFAULT_PAGE_SIZE_QUERY_PARAMETER
