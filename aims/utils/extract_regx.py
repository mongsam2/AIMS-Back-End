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


def extract_student_number(content):
    """
    입력된 문자열에서 '수험번호' 패턴 이후의 8자리 숫자를 찾아 반환하는 함수.
    """
    
    patterns = [
        r"(수\s?험\s?번\s?호\s?)?(\d{8})",
        r"(\d{8})"
    ]

    nums = []

    for pattern in patterns:
        matches = re.findall(pattern, content)
        nums.extend(matches)
 
    return list(set(nums))