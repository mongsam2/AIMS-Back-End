# import json
# from django.core.management.base import BaseCommand
# from aims.models import ValidationCriteria

# class Command(BaseCommand):
#     """
#        python manage.py load_criteria
#        ▲ 명령어로 독립 실행하여 Django Admin에 데이터베이스 테이블 자동 저장
#     """

#     def handle(self, *args, **kwargs):
#         file_path = "/data/ephemeral/home/project/aims/fixtures/validation_criteria.json"
#         try:
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 data = json.load(f)
#                 for entry in data:
#                     document_type = entry["fields"]["document_type"]
#                     v_condition = entry["fields"]["v_condition"]

#                     ValidationCriteria.objects.get_or_create(
#                         document_type=document_type,
#                         v_condition=v_condition
#                     )
#             self.stdout.write(self.style.SUCCESS("Criteria loaded successfully!"))
#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f"Error: {e}"))


import os
import json
from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    """
       python manage.py load_criteria student_criteria.json validation_criteria.json
       ▲ 명령어로 독립 실행하여 Django Admin에 데이터베이스 테이블 자동 저장
    """

    def add_arguments(self, parser):
        parser.add_argument('files', nargs='+', type=str, help='Path(s) to the JSON file(s) containing data')

    def handle(self, *args, **kwargs):
        root = "/data/ephemeral/home/project/aims/fixtures/"
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

                        # ForeignKey 처리: department 이름 → ID
                        if 'department' in fields:
                            department_name = fields['department']
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

                        obj, created = model.objects.update_or_create(
                            student_id=fields['student_id'],
                            defaults=fields
                        )

                        if document_instances:
                            obj.required_documents.set(document_instances)

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