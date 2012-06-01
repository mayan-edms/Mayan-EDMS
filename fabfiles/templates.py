import os

TEMPLATE_DIR = 'fabfiles/templates'


class Template(object):
    def open(self, filename):
        self.descriptor = open(os.path.join(TEMPLATE_DIR, filename), 'r')

    def load(self, filename, context=None):
        self.open()
        self.content = self.descriptor.read() % (context if context else {})
        
    def save_as(self, filename):
        output_descriptor = open(filename, 'w')
        output_descriptor.write(self.content)
        output_descriptor.close()
        
    def close(self):
        self.descriptor.close()
