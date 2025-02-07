
import json
import os
from django.conf import settings

from aims.tasks import get_answer_from_solar


def txt_to_html(page_texts):
    html_content = []
    for i, text in enumerate(page_texts):
        html_content.append(f'<div className="page-{i+1}">')
        for line in text.split('\n'):
            if line.strip():
                html_content.append(f'  <div>{line.strip()}</div>')
        html_content.append('</div>')
    return '\n'.join(html_content)


def extract_pages_with_keywords(html_content):
    lines = html_content.split('\n')
    pages_with_keywords = set()
    current_page = None
    keywords = [
        '<div>창의적 체험활동상황</div>',
        '<div>과목 세 부 능 력 및 특 기 사 항</div>',
        '<div>과목 특 기 사 항</div>',
        '<div>학 년 행동 특성 및 종합의견</div>'
    ]

    for line in lines:
        line = line.strip()
        if line.startswith('<div className="page-'):
            current_page = line.split('"')[1].split('-')[1]
        elif any(keyword in line for keyword in keywords):
            if current_page is not None:
                pages_with_keywords.add(int(current_page))

    return sorted(list(pages_with_keywords))


def process_with_solar(api_key, parse_response):
    prompt_file = os.path.join(settings.BASE_DIR, 'aims', 'utils', 'student_record_prompt.txt')  
    
    with open(prompt_file, 'r', encoding='utf-8') as file:
        prompt_content = file.read()

    parse_text = json.dumps(parse_response, ensure_ascii=False, indent=4)
    response = get_answer_from_solar.delay(api_key, parse_text, prompt_content)
    
    return response