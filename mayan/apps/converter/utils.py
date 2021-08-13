from .literals import TRANSFORMATION_MARKER, TRANSFORMATION_SEPARATOR
from .transformations import BaseTransformation


class IndexedDictionary:
    @classmethod
    def from_dictionary_list(
        cls, dictionary_list, klass=BaseTransformation,
        marker=TRANSFORMATION_MARKER, separator=TRANSFORMATION_SEPARATOR
    ):
        result = {}

        for index, dictionary in enumerate(dictionary_list):
            for key, value in dictionary.items():
                if key == 'name':
                    result_key = '{}{}{}{}'.format(
                        marker, str(index), separator, key
                    )
                    result[result_key] = value
                elif key == 'arguments':
                    for argument_key, argument_value in value.items():
                        result_key = '{}{}{}{}{}{}'.format(
                            marker, str(index), separator, 'argument', '__', argument_key
                        )

                        result[result_key] = argument_value

        return cls(
            dictionary=result, klass=klass, marker=marker, separator=separator
        )

    def __init__(
        self, dictionary, klass=BaseTransformation,
        marker=TRANSFORMATION_MARKER, separator=TRANSFORMATION_SEPARATOR
    ):
        self.dictionary = dictionary
        self.klass = klass
        self.marker = marker
        self.separator = separator

    def as_dictionary(self):
        result_dictionary = {}

        for key, value in self.dictionary.items():
            # Check if the entry has the marker.
            if key.startswith(self.marker):
                # Remove the marker.
                key = key[len(self.marker):]

                index, part = key.split(self.separator, 1)

                if part == 'name':
                    key = 'name'

                    result_dictionary.setdefault(index, {})
                    result_dictionary[index].update({key: value})

                elif part.startswith('argument'):
                    _, key = part.split('__')

                    result_dictionary.setdefault(
                        index, {}
                    ).setdefault('arguments', {})
                    result_dictionary[index]['arguments'].update({key: value})

        return result_dictionary

    def as_dictionary_list(self):
        result_dictionary = self.as_dictionary()
        result_dictionary_list = []

        sorted_keys = sorted(result_dictionary)

        for key in sorted_keys:
            result_dictionary_list.append(result_dictionary[key])

        return result_dictionary_list

    def as_instance_list(self):
        result_dictionary = self.as_dictionary()
        result_list = []

        sorted_keys = sorted(result_dictionary)

        for key in sorted_keys:
            entry = result_dictionary[key]

            result_list.append(
                self.klass.get(name=entry['name'])(**entry['arguments'])
            )

        return result_list
