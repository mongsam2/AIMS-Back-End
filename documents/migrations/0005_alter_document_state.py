# Generated by Django 5.1.5 on 2025-01-24 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_document_criteria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='state',
            field=models.CharField(choices=[('미제출', '미제출'), ('검토', '검토'), ('제출', '제출')], default='제출', max_length=10),
        ),
    ]
