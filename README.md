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
python create_superuser.py
python -m uvicorn app:app --reload
```

Open:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/admin`
- `http://127.0.0.1:8000/` (simple landing page)

## Bootstrapping an admin user

To access the /admin interface you need a superuser, you can do this with a script each time you delete the database or create a .env file for environment variables

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

## Default data model (before customization)

- `Category`: unique category name
- `Todo`: task text, done flag, required category, and required owner (`BaseUser`)


## API behavior

- `/api/categories/` is configured read-only.
- `/api/todos/` is ownership-scoped via `OwnedPiccoloCRUD`.
- Authenticated users can only list, read, update, and delete their own todo rows.
- The owner field is enforced server-side for todo creation and updates.


## Customizing the data model

To adapt this template for your application, you need to modify the table definitions and startup logic in `tables.py`:

If you add a new table the database should cope straight away, if you modify a table you may need to delete it from piccolo.sqlite

### 1. Replace the default tables in `tables.py`

The template includes default `Category` and `Todo` tables. Replace them with your own:

**Original (to replace):**
```python
class Category(Table):
    name = Varchar(length=255, required=True, unique=True)

class Todo(Table):
    task = Varchar(length=200, required=True)
    user = ForeignKey(references=BaseUser, null=False)
    category = ForeignKey(references=Category, null=False, help_text="Select a category")
    created = Timestamptz(default=TimestamptzNow())
    done = Boolean(default=False)
```

Change these to define the tables your application needs. Refer to [Piccolo column types](https://piccolo.readthedocs.io/en/latest/columns/index.html) for available field options.

### 2. Update `initialize_schema_and_seed()` in `tables.py`

The template includes a default schema initialization function. Modify it to create your custom tables and seed initial data:

**Original (to replace):**
```python
    # Create App Tables
    await Category.create_table(if_not_exists=True)
    await Todo.create_table(if_not_exists=True)

    # Create Default Categories 
    if not await Category.exists().where(Category.name == "Urgent"):
        await Category(name="Urgent").save()

    if not await Category.exists().where(Category.name == "Non-urgent"):
        await Category(name="Non-urgent").save()
```

Replace the table creation calls with your custom tables, and update the seed data logic to match your needs.

### 3. Update imports in `app.py`

Update the import to use your custom table classes:

**Original (to replace):**
```python
from tables import Category, Todo, initialize_schema_and_seed
```

Replace `Category` and `Todo` with your own table class names. The `initialize_schema_and_seed` function is called automatically during app startup.

### 4. Update CRUD endpoints in `app.py` (optional)

If you need API endpoints for your tables, look for the template's default endpoints and replace them with your own tables:

**Original (to replace):**
```python
FastAPIWrapper(
    root_url="/api/categories/",
    fastapi_app=app,
    piccolo_crud=PiccoloCRUD(
        table=Category, 
        read_only=True
    ),
)

FastAPIWrapper(
    root_url="/api/todos/",
    fastapi_app=app,
    piccolo_crud=OwnedPiccoloCRUD(
        table=Todo,
        read_only=False,
        owner_column=Todo.user,
    ),
)
```

Replace with endpoints for your custom tables using `PiccoloCRUD` (CRUD is an api that can do Create, Retrieve, Update & Delete or 'OwnedPiccoloCRUD' which imposes that a entity belongs to a user.

## Customizing admin setup

Use the same approach for admin: find the template code below and replace it with your own table classes and routes.

### 1. Update admin table registration in `app.py`

The admin mount controls which tables appear in Piccolo Admin.

**Original (to replace):**
```python
app.mount(
    "/admin",
    create_admin(
        tables=[Category, Todo],
        allowed_hosts=_get_allowed_hosts(),
    ),
    name="admin",
)
```

Replace `Category` and `Todo` with your own table classes (for example, your domain-specific models).

## Running (with auto reload)

```bash
python -m uvicorn app:app --reload
```

Remember if you have had to delete the database that you will need a new superuser with `python create_superuser.py` or a .env file


# More detail             

## Run tests

```bash
pytest -q
```

The tests in `tests/test_auth_todo_ownership.py` cover auth flow

## Configuration notes

- Default DB engine is SQLite (`instance/piccolo.sqlite`) via `piccolo_conf.py`.
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

