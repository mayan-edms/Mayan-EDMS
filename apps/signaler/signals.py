from django.dispatch import Signal

pre_collectstatic = Signal()
pre_update_index = Signal()
post_update_index = Signal()
