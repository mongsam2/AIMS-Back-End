# Generated by Django 5.1.5 on 2025-01-23 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aims', '0006_alter_summarization_content_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EssayRange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_value', models.IntegerField()),
                ('max_value', models.IntegerField()),
                ('penalty', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='essaycriteria',
            name='ranges',
            field=models.ManyToManyField(to='aims.essayrange'),
        ),
    ]
