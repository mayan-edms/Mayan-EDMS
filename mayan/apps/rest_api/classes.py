from __future__ import unicode_literals


class Endpoint(object):
    def __init__(self, label):
        self.label = label

    @property
    def url(self):
        return '/api/{}/'.format(self.label)
