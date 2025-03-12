# FORM 13 F 데이터 수집 파이프라인

### 개요
- 개발 환경 : FastAPI, uvicorn
- 아키텍처 : 클린아키텍처, MSA(Kafka)
- 수집 시스템 아키텍처 ```Airflow(stream) -> Uvicorn -> Kafka -> MongoDB(Local Storage) -> Kafka(fin)``` ==외부 App==> ```Kafka(fin 구독) -> MongoDB 조회 -> 외부 App DB(Shared Storage)```
- 개발 방법 : 객체지향 + FastAPI 탬플릿 혼용, TDD

### FastAPI 설치 방법
```bash
# FastAPI 라이브러리 
pip install fastapi
# FastAPI 서드파티 라이브러리
pip install fastapi-utils
pip install typing-inspect
# asyncio 비동기 처리가 가능한 서버
pip install uvicorn
```

### FastAPI 실행 방법
```bash
# app 디렉토리로 이동
cd app
# 서버 실행
uvicorn main:app --port 8001 --reload
```

### Test 진행
```bash
# pytest 설치
pip install pytest
# 비동기 요청 테스트 라이브러리
pip install trio
# test.py 만들고, 테스트 실행
pytest
# 단일 테스트 실행
pytest -k "test_get_portfolios_urls" ./tests/api/controllers/test_fillings_controller.py
```

### Kafka
```bash
pip install kafka-python
```