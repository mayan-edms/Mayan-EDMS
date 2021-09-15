import functools

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
            # Gather everything set before the wrapped function.
            event_manager.pop_event_attributes()

            if event_manager.order == EVENT_MANAGER_ORDER_BEFORE:
                event_manager.commit()

            result = func(self, *args, **kwargs)

            # Call `pop_event_attributes` again to gather anything else
            # set inside the wrappedd function itself.
            event_manager.pop_event_attributes()

            if event_manager.order == EVENT_MANAGER_ORDER_AFTER:
                event_manager.commit()

            return result
        return wrapper
    return decorator
