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
    

def is_doc_type_valid(e_type, d_type):
    if e_type == d_type:
        return True
    else: return False


def similarity(queries, text_vectors):
    """
    각 query에 대해 text_vectors와의 유사도를 계산하고 유사도 값 리스트를 반환합니다.

    Args:
        queries (list): 비교할 query 리스트
        text_vectors (list): 기준이 되는 벡터 리스트

    Returns:
        list: 각 query에 대한 유사도 값 리스트
    """
    similarity_results = []

    for query_embedding in queries:
        similarity_list = [np.dot(query_embedding, passage_embedding) for passage_embedding in text_vectors]
        similarity_results.append(similarity_list)

    return similarity_results