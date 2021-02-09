from .tasks import task_duplicates_clean_empty_lists, task_duplicates_scan_for


def handler_scan_duplicates_for(sender, instance, **kwargs):
    task_duplicates_scan_for.apply_async(
        kwargs={'document_id': instance.document_id}
    )


def handler_remove_empty_duplicates_lists(sender, **kwargs):
    task_duplicates_clean_empty_lists.apply_async()
