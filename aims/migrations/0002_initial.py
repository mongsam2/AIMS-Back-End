# Generated by Django 5.1.5 on 2025-01-28 08:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('aims', '0001_initial'),
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentpassfail',
            name='document_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reasons', to='documents.document'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.document'),
        ),
        migrations.AddField(
            model_name='essaycriteria',
            name='ranges',
            field=models.ManyToManyField(to='aims.evaluationrange'),
        ),
        migrations.AddField(
            model_name='extraction',
            name='document',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='extraction', to='documents.rawdata'),
        ),
        migrations.AddField(
            model_name='summarization',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.document'),
        ),
    ]
