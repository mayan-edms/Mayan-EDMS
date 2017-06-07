from __future__ import unicode_literals

from common.classes import PropertyHelper


class DocumentStateHelper(PropertyHelper):
    @staticmethod
    @property
    def constructor(*args, **kwargs):
        return DocumentStateHelper(*args, **kwargs)

    def get_result(self, name):
        return self.instance.workflows.get(workflow__internal_name=name)
