## 쫄 백엔드

- python version: 3.13.3
- formatting: black, isort

### 구동 방법

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 의존성 기록

```shell
pip freeze > requirements.txt
```
