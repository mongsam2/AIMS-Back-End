import json
#from django.conf import settings
#from aims.tasks import execute_embedding

from openai import OpenAI
def execute_embedding(queries, api_key):

    """
    1개 이상 100개 미만의 토큰에 대한 임베딩을 일괄 처리
    각 텍스트에 대한 토큰은 4,000 미만이어야 하고
    리스트 전체의 토큰 수는 204,800보다 작아야 한다

    Args:
        queries(list): 리스트 형태의 text
        api_key(str): 업스테이지 API 키

    Returns:
        embedding(list): 리스트 형태의 embedding 결과
    """
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.upstage.ai/v1/solar"
    )
    
    query_embedding = client.embeddings.create(
        model = "embedding-query",
        input = queries
    ).data

    embedding_list = [i.embedding for i in query_embedding]

    return embedding_list

api_key = ""
json_path = "/data/ephemeral/home/aims_be/documents/vectors/validations2.json"

"""
    1. criteria의 value 값을 추출하여
    2. Embedding 벡터를 생성하고
    3. 벡터를 vector 키로 추가하는 기능
"""

with open(json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

for document in data:
    criteria_values = list(document["criteria"])
    embeddings = execute_embedding(criteria_values, api_key)
    document["vector"] = embeddings


with open(json_path, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("JSON 파일이 성공적으로 업데이트되었습니다!")