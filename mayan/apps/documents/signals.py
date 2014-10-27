from django.dispatch import Signal

post_version_upload = Signal(providing_args=['instance'], use_caching=True)
