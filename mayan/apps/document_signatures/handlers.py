from __future__ import unicode_literals

from .tasks import (
    task_unverify_key_signatures,
    task_verify_missing_embedded_signature,
    task_verify_key_signatures
)


def handler_verify_missing_embedded_signature(sender, **kwargs):
    task_verify_missing_embedded_signature.delay()


def handler_unverify_key_signatures(sender, **kwargs):
    task_unverify_key_signatures.apply_async(
        kwargs=dict(key_id=kwargs['instance'].key_id)
    )


def handler_verify_key_signatures(sender, **kwargs):
    task_verify_key_signatures.apply_async(
        kwargs=dict(key_pk=kwargs['instance'].pk)
    )
