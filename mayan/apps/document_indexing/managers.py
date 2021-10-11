from django.db import models


class DocumentIndexInstanceNodeManager(models.Manager):
    def get_for(self, document):
        return self.filter(documents=document)


class IndexInstanceManager(models.Manager):
    def delete_empty_nodes(self):
        for index in self.all():
            index.delete_empty_nodes()

    def document_add(self, document):
        for index in self.filter(document_types=document.document_type):
            index.document_add(document=document)

    def document_remove(self, document):
        for index_instance in self.filter(index_template_nodes__index_instance_nodes__documents=document):
            index_instance.document_remove(document=document)


class IndexTemplateManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

    def rebuild(self):
        for index_template in self.all():
            index_template.rebuild()
