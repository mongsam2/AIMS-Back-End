# Generated by Django 5.1.5 on 2025-02-07 13:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aims', '0008_alter_documentpassfail_failed_conditions'),
        ('documents', '0007_documentation_issue_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentpassfail',
            name='document_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reasons', to='documents.documentation'),
        ),
    ]
