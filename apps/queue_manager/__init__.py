from queue_manager.models import Queue as QueueModel, QueuePushError

class Queue(object):
    @classmethod
    def __new__(cls, name, queue_name, label=None, unique_names=False):
        name = queue_name
        if not label:
            label=u''
        queue, created = QueueModel.objects.get_or_create(
            name=name,
            defaults={
                'label': label,
                'unique_names': unique_names
            }
        )
        if not created:
            queue.label = label
            queue.unique_names = unique_names
            queue.save()
        return queue
