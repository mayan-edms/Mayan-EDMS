from __future__ import unicode_literals

import inspect

import docutils.parsers.rst.directives.misc
from sphinx.directives.other import Include as SphinxInclude


def monkey_patch_include(substitutions):
    """
    Monkey patch docutil's Include directive to support global substitutions.
    The Include class doesn't have a hook to modify the content before
    inserting it back, so we add a call to our own transformation
    method. We patch the base Include class, recreate Sphinx's Include class,
    and register it as the new main include directive.
    All this avoids copy and paste of the original code here.
    """
    source_code = ''.join(inspect.getsourcelines(
        docutils.parsers.rst.directives.misc.Include)[0]
    )
    source_code = source_code.replace(
        'self.state_machine.insert_input(include_lines, path)',
        'include_lines=self.global_substitution(lines=include_lines)\n        self.state_machine.insert_input(include_lines, path)',
    )
    exec(source_code, docutils.parsers.rst.directives.misc.__dict__)

    class Include(docutils.parsers.rst.directives.misc.Include, SphinxInclude):
        def global_substitution(self, lines):
            result = []
            for line in lines:
                for old, new in substitutions:
                    line = line.replace(old, new)
                result.append(line)
            return result

    return Include
