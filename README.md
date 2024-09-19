# wanted_budget_management
원티드 백엔드 과제 예산 관리 어플리케이션

## Food Finder

#### **예산 관리 어플리케이션**
[[원티드 백엔드 프리온보딩 인턴십]](https://www.wanted.co.kr/events/pre_ob_be_1_seoul) - 기업 실무 프로젝트 4차 과제

> 언어 및 프레임워크 : Python 3.10 & Django 4.1, DRF 3.13.1
RDBMS: PostgreSQL 13 \
ETC Tools: Docker(Compose), Git & Github

- 기간: 24.09.10 ~ 24.09.20

<br>

**목차**
1. [프로젝트 소개](#프로젝트-소개)
2. [프로젝트 구조 및 설계](#프로젝트-구조-및-설계)
3. [주요 기능](#주요-기능)
4. [API 명세서](#API-명세서)

<br>

## 프로젝트 소개
본 서비스는 사용자들이 개인 재무를 관리하고 지출을 추적하는 데 도움을 주는 애플리케이션입니다. \
이 앱은 사용자들이 예산을 설정하고 지출을 모니터링하며 재무 목표를 달성하는 데 도움이 됩니다.  \

## 프로젝트-구조-및-설계

### ERD

### 디렉토리 구조

<details>
<summary>Directory Structure</summary>

```
├── .env
├── .gitignore
├── Dockerfile
├── README.md
├── docker-compose.yml
├── budget
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│── manage.py
│── accounts
│   │── __init__.py
│   │── migrations
│   │── models.py
│   │── serializers.py
│   │── urls.py
│   │── views


```

</details>

### Setting Guide (Docker)
* 루트 디렉토리에 `.env` 밑처럼 세팅
```
SECRET_KEY= // 자체 입력

## POSTGRES SETTINGS
POSTGRES_DB=postgres
POSTGRES_NAME=postgres
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

```
```
-- 프로젝트 경로로 이동
cd [프로젝트 경로]

-- Docker Compose build & 실행 (=> http://localhost:8000/ 경로로 접속)
docker-compose up -d

-- 컨테이너 중지 및 생성된 컨테이너 삭제
docker-compose down

-- 로컬 도커 이미지 전체 삭제
docker rmi $(docker images -q)
```
```
-- 마이그레이션 명령어
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
```

## 주요 기능
- **회원가입 및 인증**: 계정 생성, JWT를 통한 인증 및 보안 유지.
- ****: 디스코드 웹훅을 활용하여 

## API 명세서

| API 명칭                | HTTP 메서드 | 엔드포인트                                    | 설명                                                       |
|------------------------|-------------|-----------------------------------------------|------------------------------------------------------------|
| 사용자 회원가입        | POST        | /api/accounts//register/                                      | 새로운 사용자를 등록합니다.                                  |
| 사용자 로그인          | POST        | /api/accounts/login/                                      | 사용자를 로그인시킵니다.                                     |
| 사용자 로그아웃        | POST        | /api/accounts//logout/                                      | 사용자를 로그아웃시킵니다.                                   |
            |


