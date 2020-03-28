from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentpagetransformation',
            name='document_page',
        ),
        migrations.DeleteModel(
            name='DocumentPageTransformation',
        ),
    ]
