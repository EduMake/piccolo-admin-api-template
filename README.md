# Piccolo Todo API Template

FastAPI + Piccolo ORM starter template with session authentication, Piccolo Admin, and ownership-scoped CRUD for todos.

## What this template includes

- FastAPI app in `app.py`
- Data models in `tables.py`
- Piccolo Admin mounted at `/admin`
- Auth endpoints using session cookies:
  - `POST /api/session/register`
  - `POST /api/session/login`
  - `POST /api/session/logout`
  - `GET /api/session`
- Read-only categories API at `/api/categories/`
- User-owned todos API at `/api/todos/`
- Startup schema creation + seed data in `app_startup.py`

## Quick start

```bash
python -m pip install -r requirements.txt
python -m uvicorn app:app --reload
```

Open:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/admin`
- `http://127.0.0.1:8000/` (simple landing page)

## Bootstrap an admin user

Option 1 (manual script):

```bash
python create_superuser.py
```

If the username already exists, the script updates that user and ensures `admin`, `superuser`, and `active` are enabled.

Option 2 (environment variables at startup):

- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- `ADMIN_EMAIL` (optional)

On startup, if no superuser exists, the app will create one from those variables.

## Data model

- `Category`: unique category name
- `Todo`: task text, done flag, required category, and required owner (`BaseUser`)

## API behavior

- `/api/categories/` is configured read-only.
- `/api/todos/` is ownership-scoped via `OwnedPiccoloCRUD`.
- Authenticated users can only list, read, update, and delete their own todo rows.
- The owner field is enforced server-side for todo creation and updates.

## Run tests

```bash
pytest -q
```

The tests in `tests/test_auth_todo_ownership.py` cover auth flow, category read-only behavior, and todo ownership isolation.

## Configuration notes

- Default DB engine is SQLite (`instance/todo.sqlite`) via `piccolo_conf.py`.
- CORS origins can be set with `CORS_ORIGINS` as a comma-separated list.
- Render host variables are supported for admin allowed-host checks.

## Deployment

- Render blueprint config: `render.yaml`
- Render deployment guide: [RENDER_SETUP.md](RENDER_SETUP.md)
- PostgreSQL migration guide: [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md)

## Codespaces notes

- Forward port `8000` to access FastAPI endpoints.
- For external callbacks or cross-origin clients, set the forwarded port visibility as needed and include that origin in `CORS_ORIGINS`.

## Troubleshooting

- If startup fails with `ModuleNotFoundError` for `app_routes` or `htmx_routes`, either add those route modules or remove/comment those optional imports and router includes in `app.py`.

