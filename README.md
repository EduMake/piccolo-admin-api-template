# Piccolo Admin API Template

A FastAPI + Piccolo ORM starter template with:

- Piccolo models in `tables.py`
- Auto CRUD API via `piccolo_api`
- Piccolo admin mounted at `/admin`
- Session auth endpoints
- Optional server-rendered examples (`/app` and `/htmx`)

## Quick start

```bash
python -m pip install -r requirements.txt
python -m uvicorn app:app --reload
```

Open:

- `http://localhost:8000/docs`
- `http://localhost:8000/admin`

## Core idea

Edit `tables.py` and your storage schema, admin surface, and API resources evolve with the model.
