# Generated by Django 5.1.5 on 2025-01-19 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aims', '0002_inappropriatereason_delete_inappropriate_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='summarization',
            name='memo',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
