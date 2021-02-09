import uuid


# Required by migration 0010_auto_20180403_0702.py
def upload_to(instance, filename):
    return 'shared-file-{}'.format(uuid.uuid4().hex)
