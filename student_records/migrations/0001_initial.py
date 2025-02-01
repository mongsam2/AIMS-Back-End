# Generated by Django 5.1.5 on 2025-02-01 22:54

import common.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        ('students', '0002_student_required_documents'),
    ]

    operations = [
        migrations.CreateModel(
            name='Summarization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('question', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='StudentRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extraction', models.TextField(blank=True, null=True)),
                ('file', models.FileField(upload_to=common.models.upload_to)),
                ('state', models.CharField(choices=[('제출', '제출'), ('검토', '검토')], default='검토', max_length=10)),
                ('memo', models.TextField(blank=True, null=True)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('document_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.documenttype')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student')),
                ('summarization', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_record', to='student_records.summarization')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
