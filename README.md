
### 설치 필요

sudo apt update
sudo apt install -y poppler-utils      


### Git Clone

> git clone -b develop --single-branch https://github.com/mongsam2/AIMS-Back-End.git

### 가상 환경 설정

> python3 -m venv .venv                  
> source .venv/bin/activate           


### 패키지 설치

> pip3 install -r requirements.txt


### DB 생성

> python manage.py migrate


### 백엔드 서버 실행

> python manage.py runserver
   

### API 명세서      
> https://naver-boostcamp-cv-07.notion.site/Final-API-bd6ee394414d400aae99bd69b5f869d7?pvs=4                
