# Generated by Django 5.1.5 on 2025-01-19 06:51

import django.db.models.deletion
import documents.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(max_length=50)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('file_url', models.FileField(upload_to=documents.models.Document.upload_to)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student')),
            ],
        ),
    ]
