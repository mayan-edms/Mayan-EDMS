from ..classes import QuotaBackend
from ..exceptions import QuotaExceeded


class TestQuota(QuotaBackend):
    field_order = ('test_limit',)
    fields = {
        'test_limit': {
            'label': 'test limit',
            'class': 'django.forms.IntegerField',
        },
    }
    label = 'Test quota'

    def __init__(self, test_limit):
        self.test_limit = test_limit
        self.test_usage = 0

    def _allowed(self):
        return self.test_limit

    def _allowed_filter_display(self):
        return 'test limit: {}'.format(self._allowed())

    def _usage(self, **kwargs):
        return self.test_usage

    def process(self, **kwargs):
        if self._usage() > self._allowed():
            raise QuotaExceeded('Test count exceeded.')

    def usage(self):
        allowed = self._allowed()
        usage = self._usage()

        return '{usage} out of {allowed} ({percent}0.2f%%)'.format(
            allowed=allowed,
            percent=usage / allowed * 100,
            usage=usage
        )
