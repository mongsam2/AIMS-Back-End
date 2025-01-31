# Generated by Django 5.1.5 on 2025-01-31 15:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aims', '0004_extractionessay'),
        ('documents', '0006_alter_document_document_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extractionessay',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extraction_essay', to='documents.document'),
        ),
    ]
