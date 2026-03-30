### Run Server

```bash
cd backend
```

```bash
uv venv venv
```

```bash
venv\Scripts\activate
```

```bash
uv pip install -r requirements.txt
```

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

### Clean Cache

```bash
Get-ChildItem -Path . -Include **pycache** -Recurse -Force | Remove-Item -Recurse -Force
```
