# Generated by Django 5.1.5 on 2025-01-24 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aims', '0008_rename_essayrange_evaluationrange'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='memo',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
