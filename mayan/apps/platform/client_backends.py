import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from django.conf.urls import url

import mayan

from .classes import ClientBackend


class ClientBackendSentry(ClientBackend):
    _url_namespace = 'sentry'

    def get_url_patterns(self):
        def trigger_error(request):
            1 / 0

        return [
            url(
                regex=r'^debug/$', name='sentry_debug',
                view=trigger_error
            )
        ]

    def launch(self):
        self.setup_arguments()

        sentry_sdk.init(
            dsn=self.dsn,
            integrations=(DjangoIntegration(),),
            traces_sample_rate=self.traces_sample_rate,
            send_default_pii=self.send_default_pii,
            release=self.release
        )

    def setup_arguments(self):
        self.dsn = self.kwargs['dsn']

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        self.traces_sample_rate = self.kwargs.get('traces_sample_rate', 1.0)

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        self.send_default_pii = self.kwargs.get('send_default_pii', True)

        # By default the SDK will try to use the SENTRY_RELEASE
        # environment variable, or infer a git commit
        # SHA as release, however you may want to set
        # something more human-readable.
        self.release = mayan.__build_string__
