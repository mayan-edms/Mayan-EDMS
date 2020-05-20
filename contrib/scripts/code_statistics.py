#!/usr/bin/env python

import os

BASE_PATH = 'mayan/apps'


def print_views_summary(module_filename):
    with open(module_filename) as file_object:
        print('    module:', module_filename)
        count_class_based_views = 0
        count_function_based_views = 0
        for line in file_object:
            if line.startswith('class') and 'View' in line:
                count_class_based_views += 1

            if line.startswith('def') and 'request' in line:
                count_function_based_views += 1

    print('      class based views: {}'.format(count_class_based_views))
    print('      function based views: {}'.format(count_function_based_views))
    return count_class_based_views, count_function_based_views


def print_tests_summary(module_filename):
    with open(module_filename) as file_object:
        print('    module:', module_filename)
        count_tests = 0
        for line in file_object:
            if line.startswith('    def test'):
                count_tests += 1

    print('      tests: {}'.format(count_tests))
    return count_tests


if __name__ == '__main__':
    count_totals = {
        'Apps': 0,
        'Class based views': 0,
        'Function based views': 0,
        'Class based API views': 0,
        'Function based API views': 0,
        'Tests': 0,
    }

    for app_name in sorted(os.listdir(BASE_PATH)):
        if app_name != '__init__.py':
            count_totals['Apps'] += 1
            print('\n\nApp name: {}'.format(app_name))
            app_path = os.path.join(BASE_PATH, app_name)

            print('\n  Views')
            try:
                module_filename = os.path.join(app_path, 'views.py')
                count_class_based_views, count_function_based_views = print_views_summary(module_filename=module_filename)
                count_totals['Class based views'] += count_class_based_views
                count_totals['Function based views'] += count_function_based_views

            except IOError:
                # Check for multiple view files inside a view directory
                try:
                    module_path = os.path.join(app_path, 'views')
                    for module_name in os.listdir(module_path):
                        if not module_name.startswith('__init__.py') and not module_name.endswith('.pyc'):
                            module_filename = os.path.join(module_path, module_name)
                            count_class_based_views, count_function_based_views = print_views_summary(module_filename=module_filename)
                            count_totals['Class based views'] += count_class_based_views
                            count_totals['Function based views'] += count_function_based_views
                except OSError:
                    # No views directory, skip app
                    print('    No views')

            print('\n  API Views')
            try:
                module_filename = os.path.join(app_path, 'api_views.py')
                count_class_based_views, count_function_based_views = print_views_summary(module_filename=module_filename)
                count_totals['Class based API views'] += count_class_based_views
                count_totals['Function based API views'] += count_function_based_views

            except IOError:
                # No API views directory, skip app
                print('    No API views')

            print('\n  Tests')
            module_path = os.path.join(app_path, 'tests')
            try:
                for module_name in os.listdir(module_path):
                    if not module_name.startswith('__init__.py') and not module_name.endswith('.pyc'):
                        module_filename = os.path.join(module_path, module_name)
                        if module_name.startswith('test'):
                            count_tests = print_tests_summary(module_filename=module_filename)
                            count_totals['Tests'] += count_tests

            except OSError:
                # No tests directory, skip app
                print('    No tests')

    print('-' * 10)

    print('Totals:')
    for key, value in count_totals.items():
        print('  {}: {}'.format(key, value))
