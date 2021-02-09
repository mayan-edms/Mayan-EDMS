class WorkflowException(Exception):
    """Base exception for the document states app"""


class WorkflowStateActionError(WorkflowException):
    """Raise for errors during execution of workflow state actions"""
