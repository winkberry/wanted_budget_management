## budget_management

#### **예산 관리 어플리케이션**
[[원티드 백엔드 프리온보딩 인턴십]](https://www.wanted.co.kr/events/pre_ob_be_1_seoul) - 기업 실무 프로젝트 4차 과제

> 언어 및 프레임워크 : Python 3.10 & Django 4.1, DRF 3.13.1
RDBMS: PostgreSQL 13 \
ETC Tools: Docker(Compose), Git & Github

- 기간: 24.09.12 ~ 24.09.20

<br>

**목차**
1. [프로젝트 소개](#프로젝트-소개)
2. [프로젝트 구조 및 설계](#프로젝트-구조-및-설계)
3. [주요 기능](#주요-기능)
4. [API 명세서](#API-명세서)
5. [Postman Test](#Postman-Test)

<br>

## 프로젝트 소개
본 서비스는 사용자들이 개인 재무를 관리하고 지출을 추적하는 데 도움을 주는 애플리케이션입니다. \
이 앱은 사용자들이 예산을 설정하고 지출을 모니터링하며 재무 목표를 달성하는 데 도움이 됩니다. 

## 프로젝트-구조-및-설계

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
│── budget_management
│   │── __init__.py
│   │── migrations
│   │── models.py
│   │── serializers.py
│   │── urls.py
│   │── views
│── expenses
│   │── management
│   │   │──commands
│   │   │  │──scheduler.py
│   │── __init__.py
│   │── migrations
│   │── models.py
│   │── serializers.py
│   │── urls.py
│   │── views
│   │── tasks


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

-- 에러 로그 출력
docker-compose logs web

```

```
-- 마이그레이션 명령어
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
```

## 주요 기능
- **회원가입 및 인증**: 계정 생성, JWT를 통한 인증 및 보안 유지.
- **예산 설정 및 추천**: 예산 카테고리 별로 예산을 설정. 유저들이 설정한 카테고리 별 예산을 통계하여 예산을 추천.
- **지출 CRUD**: 지출을 생성, 수정, 읽기, 삭제, 합계제외.
- **지출 조회**: 필수적으로 기간으로 조회. 특정 카테고리별로 조회. 합계제외 처리한 지출은 지출 합계에서 제외.
- **데일리 지출 안내**: 오늘 지출한 내용을 총액과 카테고리 별 금액 안내. 월별 설정한 예산을 기준으로 적정 금액과 오늘 지출한 금액 안내. 카테고리 별 적정 금액, 지출금액의 차이를 위험도 퍼센테이지로 안내.
- **데일리 지출 추천**: 오늘 지출 가능한 금액, 카테고리별 오늘 지출 가능한 금액, 초과시 최소 한도 설정, 유저의 상황에 맞는 멘트 출력.

## API 명세서

| API 명칭                | HTTP 메서드 | 엔드포인트                                    | 설명                                                       |
|------------------------|-------------|-----------------------------------------------|------------------------------------------------------------|
| 사용자 회원가입        | POST        | /api/accounts//register/                                      | 새로운 사용자를 등록합니다.                                  |
| 사용자 로그인          | POST        | /api/accounts/login/                                      | 사용자를 로그인시킵니다.                                     |
| 사용자 로그아웃        | POST        | /api/accounts//logout/                                      | 사용자를 로그아웃시킵니다. (토큰 비활성화)                                  |
| 엑세스 토큰 발급       | POST        | /api/token/refresh/                                      | 엑세스 토큰 만료 시 리프레시 토큰으로 새로운 엑세스 토큰을 발급 합니다. |
| 예산 설정              | POST       | /api/budget/                                           | 예산을 카테고리 별로 설정합니다.  |
| 예산 목록 조회          | GET      | /api/budget/                                       | 카테고리 별로 설정된 예산 목록을 조회 합니다.         |
| 예산 카테고리 조회      | GET      | /api/categories/                                      | 모든 카테고리 목록을 조회 합니다.        |
| 예산 추천               | POST     | /api/budget/recommendation/                           | 총 금액을 입력하면 카테고리별 예산을 추천해 줍니다.   |
| 지출 등록  | POST | /api/expenses/create/ | 지출을 등록 합니다. (예산 설정한 카테고리 내에서) |
| 지출 내역 조회  | GET      | /api/expenses/list/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&category=category | 기본 기간 별로, 카테고리 별로 지출 내역을 조회 할 수 있습니다. 총 지출 내역과 카테고리별 총 지출 내역을 알 수 있습니다. |
| 데일리 지출 안내 | GET | /api/expenses/daily-summary/ | 오늘 총 지출 금액과 카테고리별 오늘 지출 금액, 적정 지출 금액, 위험도에 대해 알려줍니다. |
| 데일리 지출 추천 | GET | /api/expenses/daily-recommendation/ | 오늘 지출 가능한 금액 합계와 카테고리별 금액 추천, 상황별 안내 메세지. |


## Postman Test

회원가입  
1. 요청 성공  
![회원가입요청과완료_비밀번호반환안하도록수정](https://github.com/user-attachments/assets/893a4eb6-bcac-45a3-8ced-c7842325418d)  

2. 아이디가 중복 일때   
![회원가입시중복일때](https://github.com/user-attachments/assets/460f1948-31e3-46f5-af97-c0d3a21b8d1f)  

로그인
![로그인시도와성공토큰받는거](https://github.com/user-attachments/assets/d36f0f40-c169-4620-8ac9-8cb22b9c8345)

로그아웃
![로그아웃구현](https://github.com/user-attachments/assets/d65bdb22-1da0-42b7-b490-95c6aa0dd4bf)

토큰 만료시 갱신하기
- body에 리프레쉬 토큰을 실어 보내면 갱신된 엑세스 토큰을 반환함
![리프레쉬토큰으로엑세스토큰갱신](https://github.com/user-attachments/assets/b8781b2c-6da7-4e62-9ed8-c205e95e1d20)

모든 API 요청시 엑세스 토큰 필요
- 헤더에 엑세스 토큰과 함께 api 요청 보내야 함 
- 회원가입, 로그인 시 필요 없음 
![모든api요청시헤더에엑세스토큰넣어야함](https://github.com/user-attachments/assets/7c86ded0-cb81-498c-9bf1-ca18ff0e14f3)

예산 카테고리 보기
![예산카테고리목록반환성공](https://github.com/user-attachments/assets/b03d3677-255f-4019-b830-e2091b7ba142)

예산 금액 설정(List)
![여러개의예산금액설정성공](https://github.com/user-attachments/assets/4c3008b3-e161-40a9-8452-0fff28346469)

예산 금액 수정
![예산금액설정한거수정할수있음성공](https://github.com/user-attachments/assets/aa406171-26c3-48ff-96aa-656859910141)

예산 금액 설정 목록 보기
![예산금액설정한거_목록보기성공](https://github.com/user-attachments/assets/cc499719-6f23-4f0e-8f88-0c0cf41ab1f3)

예산 추천 기능
![예산추천기능성공](https://github.com/user-attachments/assets/96204262-2a63-485d-89d9-010b4d14a5df)

지출 등록
![지출등록화장품성공](https://github.com/user-attachments/assets/1b7976c7-d85d-4ae1-80cc-ed3593549d52)

지출 목록
![버스비추가한토탈지출목록내역](https://github.com/user-attachments/assets/6da2c0bd-e674-4f38-9172-b782b3d187c1)

데일리 지출 안내
- 오늘 총 지출한 금액, 카테고리별 오늘 지출한 금액과 예산 대비 적정 금액, 위험도 
![데일리오늘지출안내](https://github.com/user-attachments/assets/8079257f-eae8-4ba3-b93f-b77cf94e6c36)

데일리 지출 추천
- 오늘 지출 가능한 금액, 카테고리별 오늘 지출 가능한 금액, 초과시 최소 한도 설정, 유저의 상황에 맞는 멘트 출력
![오늘지출추천](https://github.com/user-attachments/assets/52d6cfc7-33df-45c2-8b0d-52f19639b087)





