
### 설치 필요

sudo apt update
sudo apt install -y poppler-utils

# 작성 중...

### 가상 환경 설정

python3 -m venv .venv
source .venv/bin/activate

### 패키지 설치

pip3 install -r requirements.txt

### DB 생성

python manage.py migrate

### 백엔드 서버 실행

python manage.py runserver

### API
(여기에 API 명세서 링크만 공개해서 넣을까요...?)
