# better_yaml.py

"""
Customized YAML serializer, with more condensed and readable output.
Rather than producing a flat list of objects with the same three attributes:

    - fields: {...}
      model: modelname
      pk: 123

This serializer nests the data, grouping by model name, then indexing by
primary key. For example, instead of this output, as produced by the default
YAML serializer:

    - fields: {name: blue}
      model: app.firstmodel
      pk: 3
    - fields: {name: red}
      model: app.firstmodel
      pk: 1
    - fields: {name: green}
      model: app.firstmodel
      pk: 2
    - fields: {name: crumbly}
      model: app.secondmodel
      pk: 2
    - fields: {name: squishy}
      model: app.secondmodel
      pk: 1

You'll get this output:

    app.firstmodel:
      1: {name: red}
      2: {name: green}
      3: {name: blue}
    app.secondmodel:
      1: {name: squishy}
      2: {name: crumbly}

To use this customized serializer and deserializer, save this file
somewhere in your Django project, then add this to your settings.py:

    SERIALIZATION_MODULES = {
        'yaml': 'path.to.better_yaml',
    }

Note that this serializer is NOT compatible with the default Django
YAML serializer; this one uses nested dictionaries, while the default
one uses a flat list of object dicts.

Requires PyYaml (http://pyyaml.org/), of course.
"""

from StringIO import StringIO
import yaml

from django.core.serializers.pyyaml import Serializer as YamlSerializer
from django.core.serializers.python import Deserializer as PythonDeserializer
from django.utils.encoding import smart_unicode

class Serializer (YamlSerializer):
    """
    Serialize database objects as nested dicts, indexed first by
    model name, then by primary key.
    """
    def start_serialization(self):
        self._current = None
        self.objects = {}

    def end_object(self, obj):
        model = smart_unicode(obj._meta)
        pk = obj._get_pk_val()

        if model not in self.objects:
            self.objects[model] = {}

        self.objects[model][pk] = self._current
        self._current = None


def Deserializer(stream_or_string, **options):
    """
    Deserialize a stream or string of YAML data,
    as written by the Serializer above.
    """
    if isinstance(stream_or_string, basestring):
        stream = StringIO(stream_or_string)
    else:
        stream = stream_or_string

    # Reconstruct the flat object list as PythonDeserializer expects
    # NOTE: This could choke on large data sets, since it
    # constructs the flattened data list in memory
    data = []
    for model, objects in yaml.load(stream).iteritems():
        # Add the model name back into each object dict
        for pk, fields in objects.iteritems():
            data.append({'model': model, 'pk': pk, 'fields': fields})

    # Deserialize the flattened data
    for obj in PythonDeserializer(data, **options):
        yield obj
