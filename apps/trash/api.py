from __future__ import absolute_import

from .models import TrashableModelManager, new_delete_method


trashable_models = []        
def make_trashable(model):
    trashable_models.append(model)
    #model.__class__.objects = TrashableModelManager()
    #model.__class__._default_manager = TrashableModelManager()
    #model.objects = TrashableModelManager()
    model.add_to_class('objects', TrashableModelManager())
    old_delete_method = model.delete
    model.delete = new_delete_method(old_delete_method)
    #model.add_to_class('is_in_trash', return True)
