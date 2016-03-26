from __future__ import unicode_literals

from .tasks import task_unverify_signatures, task_verify_signatures


def unverify_signatures(sender, **kwargs):
    task_unverify_signatures.apply_async(
        kwargs=dict(key_id=kwargs['instance'].key_id)
    )


def verify_signatures(sender, **kwargs):
    task_verify_signatures.apply_async(
        kwargs=dict(key_pk=kwargs['instance'].pk)
    )
