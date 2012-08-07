from django.db import models


class CustomizableQuerySetManager(models.Manager):
    # FROM: https://gist.github.com/2587518
    # AUTHOR: https://gist.github.com/fission6
    # http://docs.djangoproject.com/en/dev/topics/db/managers/#using-managers-for-related-object-access
    # Not working cause of:
    # http://code.djangoproject.com/ticket/9643
    use_for_related_fields = True

    def __init__(self, qs_class=models.query.QuerySet):
        self.queryset_class = qs_class
        super(CustomizableQuerySetManager, self).__init__()

    def get_query_set(self):
        return self.queryset_class(self.model)

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)

