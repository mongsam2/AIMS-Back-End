# Generated by Django 5.1.5 on 2025-02-04 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_remove_document_fails_documentpassfail_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentpassfail',
            name='failed_condition',
            field=models.CharField(max_length=200),
        ),
    ]
