from django.test import tag

from django_test_migrations.contrib.unittest_case import MigratorTestCase


@tag('exclude', 'migration')
class Migration0003UniqueFieldsTestCase(MigratorTestCase):
    migrate_from = ('file_metadata', '0002_documenttypesettings')
    migrate_to = ('file_metadata', '0003_auto_20191226_0606')

    def prepare(self):
        StoredDriver = self.old_state.apps.get_model(
            'file_metadata', 'StoredDriver'
        )
        StoredDriver.objects.create(
            driver_path='test.path', internal_name='test_internal_name'
        )
        StoredDriver.objects.create(
            driver_path='test.path', internal_name='test_internal_name'
        )

    def test_migration_0003(self):
        StoredDriver = self.new_state.apps.get_model(
            'file_metadata', 'StoredDriver'
        )
        self.assertEqual(StoredDriver.objects.count(), 1)
