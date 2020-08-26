import functools

from django.db import transaction

from .literals import (
    EVENT_MANAGER_ORDER_AFTER, EVENT_MANAGER_ORDER_BEFORE
)


def method_event(event_manager_class, **event_manager_kwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            event_manager = event_manager_class(
                instance=self, **event_manager_kwargs
            )
            event_manager.prepare()
            event_manager.pop_event_attributes()

            with transaction.atomic():
                if event_manager.order == EVENT_MANAGER_ORDER_BEFORE:
                    event_manager.commit()

                result = func(self, *args, **kwargs)

                if event_manager.order == EVENT_MANAGER_ORDER_AFTER:
                    event_manager.commit()

            return result
        return wrapper
    return decorator
