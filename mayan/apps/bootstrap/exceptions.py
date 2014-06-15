from __future__ import absolute_import


class ExistingData(Exception):
    """
    Raised when an attempt to execute a bootstrap setup is made and there is
    existing data that would be corrupted or damaged by the loading the 
    bootstrap's fixture.
    """
    pass


class NotABootstrapSetup(Exception):
    """
    Raised when an attempting to import a bootstrap setup without a proper
    magic number metadata
    """
    pass
