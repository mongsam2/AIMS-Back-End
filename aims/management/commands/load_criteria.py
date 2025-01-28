import os
import json
from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    """
       python manage.py load_criteria doc_type_criteria.json department.json application_type.json
       python manage.py load_criteria doc_type_criteria.json department.json application_type.json essay_penalty_criteria.json student_criteria.json validation_criteria.json essay_criteria.json
       ▲ 명령어로 독립 실행하여 Django Admin에 데이터베이스 테이블 자동 저장
    """

    def add_arguments(self, parser):
        parser.add_argument('files', nargs='+', type=str, help='Path(s) to the JSON file(s) containing data')

    def handle(self, *args, **kwargs):
        root = "/data/ephemeral/home/aims_be/aims/fixtures/"
        file_paths = [os.path.join(root, file_path) for file_path in kwargs['files']]

        for file_path in file_paths:
            self.stdout.write(self.style.WARNING(f"Processing file: {file_path}"))

            if not os.path.exists(file_path):
                self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    for entry in data:
                        model_name = entry['model']
                        fields = entry['fields']

                        try:
                            model = apps.get_model(*model_name.split('.'))
                        except LookupError:
                            self.stdout.write(self.style.ERROR(f"Model {model_name} not found. Skipping entry."))
                            continue

                        # Students 모델 처리
                        if model_name == "students.student":
                            if 'student_id' not in fields:
                                self.stdout.write(self.style.ERROR("Missing 'student_id' field. Skipping entry."))
                                continue

                            # ForeignKey 처리: department 이름 → ID
                            if 'department' in fields:
                                department_name = fields.pop('department')
                                Department = apps.get_model('students', 'Department')
                                department = Department.objects.filter(department=department_name).first()
                                if department:
                                    fields['department'] = department
                                else:
                                    self.stdout.write(self.style.ERROR(f"Department '{department_name}' not found. Skipping entry."))
                                    continue

                            # ManyToMany 처리: required_documents 이름 → 인스턴스 리스트
                            required_documents = fields.pop('required_documents', [])
                            DocumentType = apps.get_model('documents', 'DocumentType')

                            document_instances = []
                            for doc_name in required_documents:
                                doc_instance = DocumentType.objects.filter(name=doc_name).first()
                                if doc_instance:
                                    document_instances.append(doc_instance)
                                else:
                                    self.stdout.write(self.style.ERROR(f"DocumentType '{doc_name}' not found. Skipping entry."))

                            # Student 객체 생성/갱신
                            obj, created = model.objects.update_or_create(
                                student_id=fields['student_id'],
                                defaults=fields
                            )

                            # ManyToMany 관계 설정
                            if document_instances:
                                obj.required_documents.set(document_instances)

                            if created:
                                self.stdout.write(self.style.SUCCESS(f"Added to {model_name}: {fields}"))
                            else:
                                self.stdout.write(self.style.WARNING(f"Updated {model_name}: {fields}"))
                        elif model_name == 'aims.essaycriteria':
                            ranges = fields.pop('ranges', [])
                            EvaluationRange = apps.get_model('aims', 'EvaluationRange')

                            range_instances = []
                            for range_id in ranges:
                                range_instance = EvaluationRange.objects.filter(id=range_id).first()
                                if range_instance:
                                    range_instances.append(range_instance)
                                else:
                                    self.stdout.write(self.style.ERROR(f"EvaluationRange '{range_id}' not found. Skipping entry."))

                            obj, created = model.objects.update_or_create(
                                id=fields.get('id'),
                                defaults={key: value for key, value in fields.items() if key != 'id'}
                            )

                            if range_instances:
                                obj.ranges.set(range_instances)  # ManyToMany 관계 설정

                            if created:
                                self.stdout.write(self.style.SUCCESS(f"Added to {model_name}: {fields}"))
                            else:
                                self.stdout.write(self.style.WARNING(f"Duplicate ignored in {model_name}: {fields}"))

                        else:
                            obj, created = model.objects.update_or_create(
                                defaults=fields,
                                **fields
                            )

                        if created:
                            self.stdout.write(self.style.SUCCESS(
                                f"Added to {model_name}: {fields}"
                            ))
                        else:
                            self.stdout.write(self.style.WARNING(
                                f"Duplicate ignored in {model_name}: {fields}"
                            ))

                self.stdout.write(self.style.SUCCESS(f"Data from {file_path} loaded successfully!"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing {file_path}: {e}"))
