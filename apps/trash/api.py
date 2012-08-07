from __future__ import absolute_import

from common.querysets import  CustomizableQuerySet

from .models import new_delete_method, TrashableQuerySetManager

trashable_models = []        


def make_trashable(model, trash_can):
    trashable_models.append(model)
    
    old_manager = getattr(model, '_default_manager')
    model.add_to_class('objects', CustomizableQuerySet.as_manager(TrashableQuerySetManager))
    model._default_manager = model.objects
    model.add_to_class('trash_passthru', old_manager)

    old_delete_method = model.delete
    model.delete = new_delete_method(trash_can, old_delete_method)
