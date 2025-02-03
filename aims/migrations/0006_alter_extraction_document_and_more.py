# Generated by Django 5.1.5 on 2025-02-03 05:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aims', '0005_alter_extractionessay_document'),
        ('documents', '0006_alter_document_document_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extraction',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extraction', to='documents.documentation'),
        ),
        migrations.AlterField(
            model_name='summarization',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.documentation'),
        ),
    ]
