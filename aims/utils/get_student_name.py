import re


def extract_student_name(content):
    """
    OCR 결과(content)에서 학생 이름을 추출하는 함수
    """
    patterns = [
        r"성명 (?:\(한자\))?\s?([가-힣]+)",
        r"신청인:\s?([가-힣]+)",
        r"세대주 성명\s([가-힣]+)"
    ]

    names = []
    for pattern in patterns:
        matches = re.findall(pattern, content)
        names.extend(matches)

    return list(set(names))