from __future__ import unicode_literals

from ..classes import ControlCode


class ControlCodeTest(ControlCode):
    arguments = ('argument_1',)
    label = 'Test'
    name = 'test'

    def execute(self, context):
        pass


ControlCode.register(control_code=ControlCodeTest)
