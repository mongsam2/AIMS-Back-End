# Generated by Django 5.1.5 on 2025-01-27 09:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantType',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=11)),
                ('applicant_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='students.applicanttype')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.department')),
                ('required_documents', models.ManyToManyField(related_name='students', to='documents.documenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_type', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student')),
            ],
        ),
    ]
