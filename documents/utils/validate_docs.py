import numpy as np

from datetime import datetime
from django.conf import settings


def is_date_valid(date_str):
    """
    입력된 날짜가 기준 날짜보다 이전이면 False, 이후 또는 같으면 True 반환

    Args:
        date_str (str): YYYY-MM-DD 형식의 날짜 문자열

    Returns:
        bool: 유효성 검사 결과
    """
    reference_date = datetime.strptime(settings.VALID_DATE, "%Y-%m-%d")
    
    try:
        input_date = datetime.strptime(date_str, "%Y-%m-%d")
        return input_date >= reference_date

    except ValueError:
        print("잘못된 날짜 형식입니다. YYYY-MM-DD 형식으로 입력하세요.")
        return False
    

def is_doc_type_valid():
    pass


def similarity(queries, text_vectors):
    similarity_list = []
    for passage_embedding in text_vectors:
        similarity = np.dot(passage_embedding, text_vectors)
        similarity_list.append(similarity)
        
    most_similar_result = queries[np.argmax(similarity_list)]

    return most_similar_result