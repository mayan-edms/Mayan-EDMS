class ModelInstanceExtraDataAPIViewMixin:
    def __init__(self, *args, **kwargs):
        _instance_extra_data = kwargs.pop('_instance_extra_data', {})
        result =  super().__init__(*args, **kwargs)
        for key, value in _instance_extra_data.items():
            setattr(self, key, value)

        return result
