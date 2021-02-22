class ClassCollection(list):
    def get(self, **kwargs):
        return self.klass.get(**kwargs)
