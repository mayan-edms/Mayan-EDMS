from django.dispatch import Signal

node_died = Signal(providing_args=['node'])
