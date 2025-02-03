sections = {
    '창의적 체험활동상황': ['교 과 학 습 발 달 상 황'],
    '세 부 능 력 및 특 기 사 항': ['< 체육 · 예술(음악/미술) >'],
    '과목 특 기 사 항': ['[2학년]', '[3학년]', '[학년 행동 특성 및 종합의견]'],
}

def extract_sections(file_path, sections):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    extracted_texts = {key: [] for key in sections.keys()}
    current_section = None

    for line in lines:
        line = line.strip()
        if current_section:
            if any(end in line for end in sections[current_section]):
                current_section = None
            else:
                extracted_texts[current_section].append(line)
        else:
            for start in sections.keys():
                if start in line:
                    current_section = start
                    break

    # 추출된 텍스트를 합쳐서 반환
    combined_text = ""
    for key, texts in extracted_texts.items():
        combined_text += f'--- {key} ---\n'
        combined_text += '\n'.join(texts) + '\n\n'
    
    return combined_text 