from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TrashedItemManager(models.Manager):
    def is_in_trash(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        try:
            self.model.objects.get(content_type=content_type, object_id=obj.id)
        except self.model.DoesNotExist:
            return False
        else:
            return True

    def ids(self):
        return [trash_item.object_id for trash_item in self.model.objects.all()]


class TrashedItem(models.Model):
    #trashed_at = models.DateTimeField(_('Trashed at'), editable=False, blank=True, null=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = TrashedItemManager()

    def __unicode__(self):
        return unicode(self.content_object)

    def restore(self):
        self.delete()


def new_delete_method(old_delete_method):
    def delete(self, *args, **kwargs):
        trash = kwargs.pop('trash', True)

        if trash==False:
            return old_delete_method(self, *args, **kwargs)
        else:
            trashed_item = TrashedItem.objects.create(content_object=self)#, trashed_at=datetime.now())

    return delete


class TrashableModelManager(models.Manager):
    def get_query_set(self):
        print 'excluded', TrashedItem.objects.items()
        query_set = super(TrashableModelManager, self).get_query_set().exclude(pk__in=TrashedItem.objects.ids())
        return query_set
