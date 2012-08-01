class JobQueuePushError(Exception):
    pass


class JobQueueNoPendingJobs(Exception):
    pass


class JobQueueAlreadyStarted(Exception):
    pass


class JobQueueAlreadyStopped(Exception):
    pass
