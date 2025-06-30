## 쫄 백엔드

- python version: 3.13.3
- formatting: black, isort
- poetry 사용

### 구동 방법

```shell
pipx install poetry
poetry install
poetry run uvicorn app.main:app --reload
```

### 의존성 기록

```shell
poetry add uvicorn // 의존성 추가
poetry add --group dev pytest // 개발 의존성 추가
```
