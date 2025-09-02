# FORM 13 F 데이터 수집 파이프라인

### 개요
- 개발 환경 : FastAPI, uvicorn
- 아키텍처 : 클린아키텍처, MSA(Kafka)
- 수집 시스템 아키텍처 ```Airflow(stream) -> Uvicorn -> Kafka -> MongoDB(Local Storage) -> Kafka(fin)``` ==외부 App==> ```Kafka(fin 구독) -> MongoDB 조회 -> 외부 App DB(Shared Storage)```
- 개발 방법 : 객체지향 + FastAPI 탬플릿 혼용, TDD
- Spec : GCP VM e2-medium + 4GB RAM 추가, 디스크 100GB
    - FastAPI APP : 0.5 CPU, 1 RAM
    - 외부 DB : 1 CPU, 1 RAM, 디스크 20GB?
    - Zookeeper : 0.5 CPU, 0.75 RAM, 디스크 10GB?, Zookeeper 1개
    - Kafka : 1 CPU, 2.5 RAM, 디스크 10GB?, 메시지 보존기간 2일, Broker 1개
    - Airflow : 1 CPU, 2.5 RAM, 디스크 20GB? -> spot vm으로 뺄까 생각 중 (비용적 측면은 local crontab이 최고)
    - MongoDB : 1 CPU, 1 RAM, 디스크 10GB?

### 가상환경 세팅
- 개인 PC에 설치되는 라이브러리 버전 충돌 관리하기 위해 각자 가상환경을 세팅
- 모든 pip install은 각자의 가상환경에서 실행
#### 가상환경 생성
```bash
python -m venv venv
```
#### 가상환경 실행
```bash
# cmd 터미널 기준
.\venv\Scripts\activate
```

### FastAPI 설치 방법
```bash
# FastAPI 라이브러리 
pip install fastapi
# FastAPI 서드파티 라이브러리 (ex. cbv)
pip install fastapi-utils
pip install typing-inspect
# Asyncio 비동기 처리가 가능한 서버
pip install uvicorn
# App 설정
pip install pydantic-settings
```

### FastAPI 실행 방법
```bash
# app 디렉토리로 이동
cd app
# 서버 실행
uvicorn main:app --port 8001 --reload
```

### Git PR 방법
```bash
# main 브랜치 이동 후 최신 상태로 업데이트
git checkout main
git pull origin main
# 새 브랜치 생성
git checkout -b <branch-name>
# 작업 완료 후 커밋 & 푸시
# GitHub에서 PR 올리고 merge
# 작업 완료한 브랜치 삭제(로컬)
git branch -d <branch-name>
# 작업 완료한 브랜치 삭제(원격)
git push origin --delete <branch-name>
```

### Test 진행
```bash
# pytest 설치
pip install pytest
pip install trio
# 비동기 요청 테스트 라이브러리
pip install pytest-asyncio
# pytest 비동기 타임아웃 기능 라이브러리
pip install pytest-timeout
# test.py 만들고, 테스트 실행
pytest
# 단일 테스트 실행 (타임아웃이 필요할 경우)
pytest -k "test_get_portfolios_urls" ./tests/api/controllers/test_fillings_controller.py (--timeout=5)
```

### Kafka (kafka-python -> aiokafka 변경)
```bash
pip install aiokafka
```

### MongoDB 드라이버
```bash
pip install motor
```

### ODM(JPA와 같은 ORM, 다만 MongoDB는 정형화된 스키마가 없기 때문에 Object-Document Mapper라고 부름)
```bash
pip install beanie
```

### Gemini API
```bash
pip install google-generativeai
```