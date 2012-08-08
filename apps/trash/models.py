import datetime

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.managers import CustomizableQuerySetManager


class TrashCanManager(models.Manager):
    def get_or_create(self, *args, **kwargs):
        instance, created = super(TrashCanManager, self).get_or_create(*args, **kwargs)
        instance.label = kwargs.get('defaults', {}).get('label')
        instance.save()
        return instance, created
        
        
class TrashCan(models.Model):
    trash_can_labels = {}
    
    name = models.CharField(max_length=32, verbose_name=_(u'name'), unique=True)
        
    objects = TrashCanManager()

    def __unicode__(self):
        return unicode(self.label) or self.names

    def _get_label(self):
        return TrashCan.trash_can_labels.get(self.name)

    def _set_label(self, value):
        TrashCan.trash_can_labels[self.name] = value

    label = property(_get_label, _set_label)

    def put(self, obj):
        # TODO: check if obj is trashable model
        obj.delete()

    @property
    def items(self):
        return self.trashcanitem_set
        
    def empty(self):
        self.items.all().delete()
        
    def save(self, *args, **kwargs):
        label = getattr(self, 'label', None)
        if label:
            TrashCan.trash_can_labels[self.name] = label
        return super(TrashCan, self).save(*args, **kwargs)
       
    class Meta:
        verbose_name = _(u'trash can')
        verbose_name_plural = _(u'trash cans')


class TrashCanItemManager(models.Manager):
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


class TrashCanItem(models.Model):
    trash_can = models.ForeignKey(TrashCan, verbose_name=_(u'trash can'))
    trashed_at = models.DateTimeField(verbose_name=_(u'trashed at'), editable=False)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = TrashCanItemManager()

    def __unicode__(self):
        return unicode(self.content_object)

    def restore(self):
        self.delete()
        
    def purge(self):
        self.content_object.delete(trash=False)
        self.delete()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.trashed_at=datetime.datetime.now()
        return super(TrashCanItem, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = _(u'trash can item')
        verbose_name_plural = _(u'trash can items')
        unique_together = ('trash_can', 'content_type', 'object_id')


class TrashableQuerySetManager(CustomizableQuerySetManager):
    def get_query_set(self):
        return super(TrashableQuerySetManager, self).get_query_set().exclude(pk__in=TrashCanItem.objects.ids())


def new_delete_method(trash_can, old_delete_method):
    def delete(self, *args, **kwargs):
        trash = kwargs.pop('trash', True)

        if trash==False:
            return old_delete_method(self, *args, **kwargs)
        else:
            #trashed_item = TrashedItem.objects.create(trash_can=trash_can, content_object=self, trashed_at=datetime.datetime.now())
            trashed_item = trash_can.items.create(trash_can=trash_can, content_object=self)

    return delete

