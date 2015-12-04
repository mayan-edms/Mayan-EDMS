from __future__ import unicode_literals

from rest_framework.filters import BaseFilterBackend


class RecentSearchUserFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_staff or request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(user=self.request.user)
