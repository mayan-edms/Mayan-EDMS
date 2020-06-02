from .classes import Layer


class LayerViewMixin:
    def dispatch(self, request, *args, **kwargs):
        self.layer = self.get_layer()
        return super(LayerViewMixin, self).dispatch(
            request=request, *args, **kwargs
        )

    def get_layer(self):
        return Layer.get(
            name=self.kwargs['layer_name']
        )
