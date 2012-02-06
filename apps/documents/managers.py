from __future__ import absolute_import

from ast import literal_eval

from django.db import models


class DocumentPageTransformationManager(models.Manager):
    def get_for_document_page(self, document_page):
        return self.model.objects.filter(document_page=document_page)

    def get_for_document_page_as_list(self, document_page):
        warnings = []
        transformations = []
        for transformation in self.get_for_document_page(document_page).values('transformation', 'arguments'):
            try:
                transformations.append(
                    {
                        'transformation': transformation['transformation'],
                        'arguments': literal_eval(transformation['arguments'].strip())
                    }
                )
            except (ValueError, SyntaxError), e:
                warnings.append(e)

        return transformations, warnings
