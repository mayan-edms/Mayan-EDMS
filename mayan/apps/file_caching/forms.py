from mayan.apps.views.forms import DetailForm

from .models import Cache, CachePartition


class CacheDetailForm(DetailForm):
    class Meta:
        fields = ('defined_storage_name',)
        model = Cache


class CachePartitionDetailForm(DetailForm):
    class Meta:
        fields = ('cache', 'name')
        model = CachePartition
