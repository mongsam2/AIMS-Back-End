# Generated by Django 5.1.5 on 2025-01-23 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aims', '0005_essaycriteria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summarization',
            name='content',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='summarization',
            name='question',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
