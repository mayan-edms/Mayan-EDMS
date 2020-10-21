from rest_framework import pagination

from .literals import (
    DEFAULT_MAX_PAGE_SIZE, DEFAULT_PAGE_SIZE,
    DEFAULT_PAGE_SIZE_QUERY_PARAMETER
)


class MayanPageNumberPagination(pagination.PageNumberPagination):
    max_page_size = DEFAULT_MAX_PAGE_SIZE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = DEFAULT_PAGE_SIZE_QUERY_PARAMETER
