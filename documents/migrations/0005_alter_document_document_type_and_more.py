# Generated by Django 5.1.5 on 2025-01-29 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_alter_documentation_student_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document_type',
            field=models.CharField(choices=[('학생생활기록부', '학생생활기록부'), ('검정고시합격증명서', '검정고시합격증명서'), ('생활기록부대체양식', '생활기록부대체양식'), ('기초생활수급자증명서', '기초생활수급자증명서'), ('주민등록초본', '주민등록초본'), ('국민체력100인증서', '국민체력100인증서'), ('체력평가', '체력평가'), ('논술', '논술'), ('알수없음', '알수없음')], default='알수없음', max_length=50),
        ),
        migrations.AlterField(
            model_name='documentation',
            name='document_type',
            field=models.CharField(choices=[('학생생활기록부', '학생생활기록부'), ('검정고시합격증명서', '검정고시합격증명서'), ('생활기록부대체양식', '생활기록부대체양식'), ('기초생활수급자증명서', '기초생활수급자증명서'), ('주민등록초본', '주민등록초본'), ('국민체력100인증서', '국민체력100인증서'), ('체력평가', '체력평가'), ('논술', '논술'), ('알수없음', '알수없음')], default='알수없음', max_length=50),
        ),
    ]
