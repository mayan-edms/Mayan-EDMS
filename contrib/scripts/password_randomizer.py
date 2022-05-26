#!/usr/bin/env python

import secrets

PASSWORD_LENGTH = 24
PASSWORD_MARKER = '_PASSWORD_START_MARKER'

with open(file='.env') as file_object:
    password_block = False
    while True:
        line = file_object.readline()

        if not line:
            break

        if PASSWORD_MARKER in line:
            password_block = True
            line = file_object.readline()
            print('# Randomly generated passwords and usernames.')

        if password_block:
            if not line.strip():
                password_block = False
            else:
                variable_name = line.strip().split('#')[-1].strip()

                print('{}"{}"'.format(
                    variable_name, secrets.token_urlsafe(PASSWORD_LENGTH))
                )
