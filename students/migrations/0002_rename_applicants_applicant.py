# Generated by Django 5.1.5 on 2025-01-18 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Applicants',
            new_name='Applicant',
        ),
    ]
