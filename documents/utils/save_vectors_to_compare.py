import json
from django.conf import settings
from aims.tasks import execute_embedding


api_key = settings.API_KEY
json_path = "/data/ephemeral/home/aims_be/documents/vectors/validations.json"

"""
    1. criteria의 value 값을 추출하여
    2. Embedding 벡터를 생성하고
    3. 벡터를 vector 키로 추가하는 기능
"""

with open(json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

for document in data:
    criteria_values = list(document["criteria"].values())
    embeddings = execute_embedding(criteria_values, api_key)
    document["vector"] = embeddings


with open(json_path, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("JSON 파일이 성공적으로 업데이트되었습니다!")