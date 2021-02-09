from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('acls', '0003_auto_20180402_0339'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalAccessControlListProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('acls.accesscontrollist',),
        ),
        migrations.AlterField(
            model_name='accesscontrollist',
            name='role',
            field=models.ForeignKey(help_text='Role to which the access is granted for the specified object.', on_delete=django.db.models.deletion.CASCADE, related_name='acls', to='permissions.Role', verbose_name='Role'),
        ),
    ]
