class DocumentNotCheckedOut(Exception):
    """
    Raised when trying to checkin a document that is not checkedout
    """
    pass


class DocumentAlreadyCheckedOut(Exception):
    """
    Raised when trying to checkout an already checkedout document
    """
    pass
