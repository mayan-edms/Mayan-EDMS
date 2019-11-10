from __future__ import unicode_literals


def get_source_read_callback(substitutions):
    def global_substitution_function(app, docname, source):
        for old, new in substitutions:
            source[0] = source[0].replace(old, new)
    return global_substitution_function
