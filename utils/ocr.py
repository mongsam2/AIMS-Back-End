import requests
import json
 
api_key = "up_i5WhoWFjRhUXflOznB9DLOMQLcG8n"

filename = "essay_20250001.pdf"
filepath = "/data/ephemeral/home/aims/databases/" + filename
 
url = "https://api.upstage.ai/v1/document-ai/ocr"
headers = {"Authorization": f"Bearer {api_key}"}

# upstage api
with open(filepath, "rb") as file:
    files = {"document": file}
    response = requests.post(url, headers=headers, files=files)



if response.status_code == 200:
    result_filename = filepath + f"ocr_result_{filename.split('.')[0]}.json"
    with open(result_filename, "w", encoding="utf-8") as result_file:
        json.dump(response.json(), result_file, ensure_ascii=False, indent=4)
    print(f"OCR 처리 성공: {result_filename}")
else:
    print(f"OCR 처리 실패: {response.status_code}, {response.text}")