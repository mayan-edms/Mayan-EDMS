import sys, pdb

previous_except_hook = None


def except_hook(exctype, value, traceback):
    if previous_except_hook:
        previous_except_hook(exctype, value, traceback)

    pdb.post_mortem(traceback)


def insert_pdb_exception_hook():
    previous_except_hook = sys.excepthook
    sys.excepthook = except_hook

