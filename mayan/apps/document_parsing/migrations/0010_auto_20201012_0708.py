from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('document_parsing', '0009_auto_20201012_0708'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentfilepagecontent',
            options={'verbose_name': 'Document file page content', 'verbose_name_plural': 'Document file page contents'},
        ),
        migrations.AlterField(
            model_name='documentfilepagecontent',
            name='document_file_page',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='content', to='documents.DocumentFilePage', verbose_name='Document file page'),
        ),
    ]
