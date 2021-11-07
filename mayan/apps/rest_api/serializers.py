from rest_framework import serializers as rest_framework_serializers
from rest_framework.fields import (  # NOQA
    BooleanField, CharField, ChoiceField, DateField, DateTimeField, DecimalField,
    DictField, DurationField, EmailField, Field, FileField, FilePathField, FloatField,
    HiddenField, HStoreField, IPAddressField, ImageField, IntegerField, JSONField,
    ListField, ModelField, MultipleChoiceField, NullBooleanField, ReadOnlyField,
    RegexField, SerializerMethodField, SlugField, TimeField, URLField, UUIDField,
)
from rest_framework.serializers import (
    HyperlinkedModelSerializer as RESTFrameworkHyperlinkedModelSerializer,
    ModelSerializer as RESTFrameworkModelSerializer
)
from rest_framework.relations import (  # NOQA
    HyperlinkedIdentityField, HyperlinkedRelatedField, ManyRelatedField,
    PrimaryKeyRelatedField, RelatedField, SlugRelatedField, StringRelatedField,
)
from rest_framework.reverse import reverse

from .serializer_mixins import DynamicFieldListSerializerMixin


class Serializer(
    DynamicFieldListSerializerMixin, rest_framework_serializers.Serializer
):
    """Serializer subclass to add Mayan specific mixins."""


class HyperlinkedModelSerializer(
    DynamicFieldListSerializerMixin, RESTFrameworkHyperlinkedModelSerializer
):
    """HyperlinkedModelSerializer subclass to add Mayan specific mixins."""


class ModelSerializer(DynamicFieldListSerializerMixin, RESTFrameworkModelSerializer):
    """ModelSerializer subclass to add Mayan specific mixins."""


class BlankSerializer(Serializer):
    """Serializer for the object action API view."""


class EndpointSerializer(Serializer):
    label = CharField(read_only=True)
    url = SerializerMethodField()

    def get_url(self, instance):
        if instance.viewname:
            return reverse(
                kwargs=instance.kwargs, viewname=instance.viewname,
                request=self.context['request'],
                format=self.context['format']
            )


class ProjectInformationSerializer(Serializer):
    __title__ = CharField(read_only=True)
    __version__ = CharField(read_only=True)
    __build__ = CharField(read_only=True)
    __build_string__ = CharField(read_only=True)
    __django_version__ = CharField(read_only=True)
    __author__ = CharField(read_only=True)
    __author_email__ = CharField(read_only=True)
    __description__ = CharField(read_only=True)
    __license__ = CharField(read_only=True)
    __copyright__ = CharField(read_only=True)
    __website__ = CharField(read_only=True)
