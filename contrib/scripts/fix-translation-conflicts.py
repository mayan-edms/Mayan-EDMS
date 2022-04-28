#!/usr/bin/env python

from pathlib import Path
from shutil import copyfileobj
from tempfile import NamedTemporaryFile


class AutomaticTranslationConflictSolver:
    """
    Performs resolution for simple translation merge conflicts.
    Example:

    <<<<<<< HEAD
    "POT-Creation-Date: 2022-04-01 05:54+0000\n"
    "PO-Revision-Date: 2022-02-03 10:14+0000\n"
    "Last-Translator: user <email.com>, 2022\n"
    =======
    "POT-Creation-Date: 2022-03-03 10:19+0000\n"
    "PO-Revision-Date: 2021-04-11 06:32+0000\n"
    "Last-Translator: user <email.com>, 2021\n"
    >>>>>>> origin/series/4.1
    """
    @staticmethod
    def handle_conflict(file_object, file_object_temporary):
        flag_remote = False

        while True:
            line = file_object.readline()

            if line == '=======\n':
                flag_remote = True

            if flag_remote:
                if '>>>>>>> origin' in line:
                    break
            else:
                file_object_temporary.write(line)

    def run(self):
        path = Path('.')
        path.lstat()

        iterator = path.rglob(pattern='*.po')

        for entry in iterator:
            if entry.is_file() or entry.is_symlink():
                with entry.open(mode='r+') as file_object:
                    with NamedTemporaryFile(mode='w+') as file_object_temporary:
                        while True:
                            line = file_object.readline()
                            if not line:
                                file_object_temporary.seek(0)
                                file_object.seek(0)
                                copyfileobj(fsrc=file_object_temporary, fdst=file_object)
                                file_object.truncate()
                                break

                            if line == '<<<<<<< HEAD\n':
                                print('Conflict found: {}'.format(entry))
                                AutomaticTranslationConflictSolver.handle_conflict(file_object, file_object_temporary)
                            else:
                                file_object_temporary.write(line)


if __name__ == '__main__':
    resolver = AutomaticTranslationConflictSolver()
    resolver.run()
