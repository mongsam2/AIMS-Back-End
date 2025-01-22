import requests
import json
import os
from openai import OpenAI

api_key = os.environ.get('UPSTAGE_API_KEY')

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

def parse_selected_pages(file_path, pages):
    url = "https://api.upstage.ai/v1/document-ai/document-parse"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    page_numbers = ','.join(map(str, pages))
    data = {"ocr": "force", "base64_encoding": '["table"]', "pages": page_numbers}
    
    with open(file_path, "rb") as file:
        files = {"document": file}
        response = requests.post(url, headers=headers, files=files, data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'PDF 파싱 실패', 'status_code': response.status_code}

def process_with_solar(parse_response):
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.upstage.ai/v1/solar"
    )

    with open('/Users/jaehyo/Desktop/ipsi/upstage/student_record_prompt.txt', 'r', encoding='utf-8') as file:
        prompt_content = file.read()

    parse_text = json.dumps(parse_response, ensure_ascii=False, indent=4)

    stream = client.chat.completions.create(
        model="solar-pro",
        messages=[
            {
                "role": "system",
                "content": prompt_content
            },
            {
                "role": "user",
                "content": parse_text
            }
        ],
        stream=False,
    )
    
    return stream.choices[0].message.content 