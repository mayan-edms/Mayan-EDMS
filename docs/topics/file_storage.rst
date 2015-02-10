============
File storage
============

The files are stored and placed under **Mayan EDMS** "control" to avoid
filename clashes (each file gets renamed to its UUID and without extension)
and stored in a simple flat arrangement in a directory. This doesn't
stop access to the files but it is not recommended because moving,
renaming or updating the files directly would throw the database out
of sync.

**Mayan EDMS** components are as decoupled from each other as possible,
storage in this case is very decoupled and its behavior is controlled
not by the project but by the Storage progamming class. Why this design?
All the other parts don't make any assumptions about the actual file
storage, files can be saved locally, over the network or even across the
internet and everything will still operate exactly the same.
