# FORM 13 F 데이터 수집 파이프라인

### 개요
- 개발 환경 : FastAPI, uvicorn
- 아키텍처 : 클린아키텍처, MSA
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
uvicorn main:app --port 8001 --reload
```