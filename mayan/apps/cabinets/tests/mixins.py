from __future__ import unicode_literals

from ..models import Cabinet

from .literals import (
    TEST_CABINET_CHILD_LABEL, TEST_CABINET_LABEL, TEST_CABINET_LABEL_EDITED
)


class CabinetAPIViewTestMixin(object):
    def _request_test_cabinet_create_api_view(self, extra_data=None):
        data = {'label': TEST_CABINET_LABEL}

        if extra_data:
            data.update(extra_data)

        # Typecast to list to force queryset evaluation
        values = list(Cabinet.objects.values_list('pk', flat=True))

        response = self.post(viewname='rest_api:cabinet-list', data=data)

        self.test_cabinet = Cabinet.objects.exclude(pk__in=values).first()

        return response

    def _request_test_cabinet_delete_api_view(self):
        return self.delete(
            viewname='rest_api:cabinet-detail', kwargs={
                'pk': self.test_cabinet.pk
            }
        )

    def _request_test_cabinet_document_remove_api_view(self):
        return self.delete(
            viewname='rest_api:cabinet-document', kwargs={
                'pk': self.test_cabinet.pk, 'document_pk': self.test_document.pk
            }
        )

    def _request_test_cabinet_edit_api_patch_view(self):
        return self.patch(
            data={'label': TEST_CABINET_LABEL_EDITED}, kwargs={
                'pk': self.test_cabinet.pk
            }, viewname='rest_api:cabinet-detail'
        )

    def _request_test_cabinet_edit_api_put_view(self):
        return self.put(
            data={'label': TEST_CABINET_LABEL_EDITED}, kwargs={
                'pk': self.test_cabinet.pk
            }, viewname='rest_api:cabinet-detail'
        )

    def _request_test_cabinet_list_api_view(self):
        return self.get(viewname='rest_api:cabinet-list')


class CabinetTestMixin(object):
    def _create_test_cabinet(self):
        self.test_cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

    def _create_test_cabinet_child(self):
        self.test_cabinet_child = Cabinet.objects.create(
            label=TEST_CABINET_CHILD_LABEL, parent=self.test_cabinet
        )


class CabinetViewTestMixin(object):
    def _request_test_cabinet_create_view(self):
        # Typecast to list to force queryset evaluation
        values = list(Cabinet.objects.values_list('pk', flat=True))

        response = self.post(
            'cabinets:cabinet_create', data={
                'label': TEST_CABINET_LABEL
            }
        )

        self.test_cabinet = Cabinet.objects.exclude(pk__in=values).first()

        return response

    def _request_test_cabinet_delete_view(self):
        return self.post(
            viewname='cabinets:cabinet_delete', kwargs={
                'pk': self.test_cabinet.pk
            }
        )

    def _request_test_cabinet_edit_view(self):
        return self.post(
            viewname='cabinets:cabinet_edit', kwargs={
                'pk': self.test_cabinet.pk
            }, data={
                'label': TEST_CABINET_LABEL_EDITED
            }
        )

    def _request_test_cabinet_child_create_view(self):
        return self.post(
            viewname='cabinets:cabinet_child_add', kwargs={
                'pk': self.test_cabinet.pk
            }, data={'label': TEST_CABINET_CHILD_LABEL}
        )

    def _request_test_cabinet_child_delete_view(self):
        return self.post(
            viewname='cabinets:cabinet_delete', kwargs={
                'pk': self.test_cabinet_child.pk
            }
        )

    def _request_test_cabinet_list_view(self):
        return self.get(viewname='cabinets:cabinet_list')

    def _request_test_document_cabinet_multiple_remove_view(self):
        return self.post(
            viewname='cabinets:document_cabinet_remove', kwargs={
                'pk': self.test_document.pk
            }, data={
                'cabinets': (self.test_cabinet.pk,),
            }
        )

    def _request_test_document_multiple_cabinet_multiple_add_view_cabinet(self):
        return self.post(
            viewname='cabinets:document_multiple_cabinet_add', data={
                'id_list': (self.test_document.pk,),
                'cabinets': self.test_cabinet.pk
            }
        )
