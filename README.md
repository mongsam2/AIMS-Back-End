
### 1. 설치 필요

```bash
sudo apt update
sudo apt install -y poppler-utils      
```

### 2. Git Clone

```bash
git clone -b develop --single-branch https://github.com/mongsam2/AIMS-Back-End.git
```

### 3. 가상 환경 설정

```bash
python3 -m venv .venv                  
source .venv/bin/activate           
```

### 4. 패키지 설치

```bash
pip3 install -r requirements.txt
```

### 5. DB 생성

```bash
python manage.py migrate
```

### 6. 백엔드 서버 실행

```bash
python manage.py runserver
```

### API 명세서
[API 명세서](https://naver-boostcamp-cv-07.notion.site/Final-API-bd6ee394414d400aae99bd69b5f869d7?pvs=4) (링크)              
