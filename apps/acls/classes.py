from common.classes import EncapsulatedObject


class AccessHolder(EncapsulatedObject):
    source_object_name = u'holder_object'


class AccessObject(EncapsulatedObject):
    source_object_name = u'obj'


class AccessObjectClass(EncapsulatedObject):
    source_object_name = u'cls'


class ClassAccessHolder(EncapsulatedObject):
    source_object_name = u'class_holder'
