class AlreadyScheduled(Exception):
    """
    Raised when trying to schedule a Job instance of anything after it was
    already scheduled in any other scheduler
    """
    pass


class UnknownJobClass(Exception):
    """
    Raised when trying to schedule a Job that is not of a a type:
    IntervalJob or DateJob
    """
    pass
