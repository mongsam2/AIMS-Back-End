from .upstage import get_answer_from_solar
from django.conf import settings
from student_records.models import Summarization
import os

def summarization_content(extraction, api_key, department):

        prompt_file = os.path.join(settings.BASE_DIR, 'prompts', 'summarization.txt')  
        with open(prompt_file, 'r', encoding='utf-8') as file:
            prompt_content = str(file.read())
        prompt_content = prompt_content.strip().replace("{지원학과}", department)
        response = get_answer_from_solar(api_key, extraction, prompt_content)

        return response

def summarization_question(extraction, api_key):

    prompt_file = os.path.join(settings.BASE_DIR, 'prompts', 'question.txt')  
    with open(prompt_file, 'r', encoding='utf-8') as file:
        prompt_content = str(file.read())

    response = get_answer_from_solar(api_key, extraction, prompt_content)

    return response