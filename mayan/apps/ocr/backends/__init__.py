class BackendBase(object):
    def execute(self, input_filename, language=None):
        raise NotImplementedError
