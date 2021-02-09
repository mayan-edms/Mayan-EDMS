from django.db.models import Max


class HooksModelMixin:
    @classmethod
    def _execute_hooks(cls, hook_list, **kwargs):
        result = None

        for hook in hook_list:
            result = hook(**kwargs)
            if result:
                kwargs.update(result)

        return result

    @classmethod
    def _insert_hook_entry(cls, hook_list, func, order=None):
        order = order or len(hook_list)
        hook_list.insert(order, func)


class PagedModelMixin:
    def get_pages_last_number(self):
        last_page_number = self.siblings.aggregate(
            page_number_maximum=Max('page_number')
        )['page_number_maximum']

        return last_page_number

    @property
    def siblings(self):
        filter_kwargs = {
            self._paged_model_parent_field: getattr(self, self._paged_model_parent_field)
        }

        return self._meta.default_manager.filter(**filter_kwargs)
