from pathlib import Path as OriginalPath


class Path(type(OriginalPath())):
    """
    TODO: Remove this class when the minimum required Python version
    becomes 3.9.
    """

    def is_relative_to(self, *other):
        """
        Backported method for Python < 3.9.
        Return whether or not this path is relative to the other path.
        https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.is_relative_to
        """
        try:
            self.relative_to(*other)
        except ValueError:
            return False
        else:
            return True
