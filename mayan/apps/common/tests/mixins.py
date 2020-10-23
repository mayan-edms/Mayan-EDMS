from ..classes import ModelCopy


class CommonAPITestMixin:
    def _request_content_type_list_api_view(self):
        return self.get(viewname='rest_api:content-type-list')


class CommonViewTestMixin:
    def _request_about_view(self):
        return self.get(viewname='common:about_view')


class ObjectCopyTestMixin:
    _test_copy_method = None

    def test_copy_method(self, exclude_fields=None, test_object=None, test_object_copy=None):
        exclude_fields = exclude_fields or ()

        if not test_object:
            test_object = self.test_object

        model_copy = ModelCopy.get(model=test_object._meta.model)
        if not test_object_copy:
            test_object_copy = test_object.copy_instance()

        if test_object == test_object_copy:
            return

        if self._test_copy_method:
            test_objects = zip(
                getattr(test_object, self._test_copy_method)(),
                getattr(test_object_copy, self._test_copy_method)()
            )
        else:
            test_objects = ((test_object, test_object_copy),)

        for test_object, test_object_copy in test_objects:
            for field in model_copy.fields:
                if field not in exclude_fields:
                    if field in model_copy.fields_reverse_related:
                        related_test_objects = zip(
                            getattr(test_object, field).all(),
                            getattr(test_object_copy, field).all()
                        )
                        exclude_fields = exclude_fields + (
                            test_object._meta.get_field(field).remote_field.name,
                        )

                        for related_test_object, related_test_object_copy in related_test_objects:
                            self.test_copy_method(
                                exclude_fields=exclude_fields,
                                test_object=related_test_object,
                                test_object_copy=related_test_object_copy
                            )
                    elif field in model_copy.fields_foreign_keys:
                        related_test_objects = (
                            (
                                getattr(test_object, field),
                                getattr(test_object_copy, field)
                            ),
                        )
                        exclude_fields = exclude_fields + (
                            test_object._meta.get_field(field).remote_field.name,
                        )

                        for related_test_object, related_test_object_copy in related_test_objects:
                            self.test_copy_method(
                                exclude_fields=exclude_fields,
                                test_object=related_test_object,
                                test_object_copy=related_test_object_copy
                            )
                    elif field in model_copy.fields_related_one_to_one:
                        related_test_objects = (
                            (
                                getattr(test_object, field),
                                getattr(test_object_copy, field)
                            ),
                        )
                        exclude_fields = exclude_fields + (
                            test_object._meta.get_field(field).remote_field.name,
                        )

                        for related_test_object, related_test_object_copy in related_test_objects:
                            self.test_copy_method(
                                exclude_fields=exclude_fields,
                                test_object=related_test_object,
                                test_object_copy=related_test_object_copy
                            )
                    else:
                        original_value = test_object._meta.default_manager.filter(
                            pk=test_object.pk
                        ).values_list(field, flat=True).first()

                        try:
                            conditional = model_copy.unique_conditional[field]
                        except KeyError:
                            """This field has no conditional entry"""
                        else:
                            new_instance_dictionary = test_object_copy.__dict__.copy()
                            if new_instance_dictionary[field].endswith('_1'):
                                new_instance_dictionary[field] = new_instance_dictionary[field][:-2]
                                if conditional(
                                    instance=test_object, new_instance_dictionary=new_instance_dictionary
                                ):
                                    original_value = '{}_1'.format(original_value)

                        if field in model_copy.fields_unique:
                            original_value = '{}_1'.format(original_value)

                        copy_value = test_object_copy._meta.default_manager.filter(
                            pk=test_object_copy.pk
                        ).values_list(field, flat=True).first()

                        self.assertEqual(original_value, copy_value)


class ObjectCopyViewTestMixin:
    def _request_object_copy_view(self):
        return self.post(
            kwargs=self.test_object_view_kwargs, viewname='common:object_copy'
        )
