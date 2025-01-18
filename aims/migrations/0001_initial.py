# Generated by Django 5.1.5 on 2025-01-18 17:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('documents', '0002_alter_document_file_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.document')),
            ],
        ),
        migrations.CreateModel(
            name='Inappropriate_Reason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('page', models.IntegerField()),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.document')),
            ],
        ),
        migrations.CreateModel(
            name='Summarization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('question', models.TextField()),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.document')),
            ],
        ),
    ]
