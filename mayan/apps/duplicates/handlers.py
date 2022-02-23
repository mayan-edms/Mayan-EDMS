from .tasks import task_duplicates_clean_empty_lists, task_duplicates_scan_for


def handler_scan_duplicates_for_document(sender, instance, **kwargs):
    print("### instance", instance)
    task_duplicates_scan_for.apply_async(
        kwargs={'document_id': instance.pk}
    )


def handler_scan_duplicates_for_document_file(sender, instance, **kwargs):
    handler_scan_duplicates_for_document(
        sender=sender, instance=instance.document
    )


def handler_remove_empty_duplicates_lists(sender, **kwargs):
    task_duplicates_clean_empty_lists.apply_async()
