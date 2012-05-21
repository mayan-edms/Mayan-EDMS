from django.dispatch import Signal

pre_collectstatic = Signal()
pre_update_index = Signal(providing_args=['mayan_runtime'])
post_update_index = Signal(providing_args=['mayan_runtime'])
