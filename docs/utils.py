from __future__ import unicode_literals


def load_env_file(filename='../config.env'):
    result = {}
    with open(filename) as file_object:
        for line in file_object:
            if not line.startswith('#'):
                key, value = line.strip().split('=')
                result[key] = value

    return result


def generate_substitutions(dictionary):
    result = []

    for key, value in dictionary.items():
        result.append(('|{}|'.format(key), value))

    return result
