from .runtime import cache


def handler_document_cache_delete(sender, **kwargs):
    cache.clear_document(document=kwargs['instance'])


def handler_node_cache_delete(sender, **kwargs):
    cache.clear_node(node=kwargs['instance'])
