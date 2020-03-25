import yaml

try:
    from yaml import CSafeLoader as SafeLoader, CSafeDumper as SafeDumper
except ImportError:
    from yaml import SafeLoader, SafeDumper


def yaml_dump(*args, **kwargs):
    defaults = {'Dumper': SafeDumper}
    defaults.update(kwargs)

    return yaml.dump(*args, **defaults)


def yaml_load(*args, **kwargs):
    defaults = {'Loader': SafeLoader}
    defaults.update(kwargs)

    return yaml.load(*args, **defaults)
