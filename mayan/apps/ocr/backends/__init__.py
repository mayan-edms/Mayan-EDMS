class BackendBase(object):
    def execute(self, input_filename, language=None):  # NOQA
        raise NotImplementedError
