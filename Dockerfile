FROM python:3.10-slim

# 작업 디렉터리 설정
WORKDIR /app

# 필요 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 파일 복사
COPY . .

# 포트 노출 및 서버 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]