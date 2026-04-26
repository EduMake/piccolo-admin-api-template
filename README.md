# Piccolo Admin API Template

A FastAPI + Piccolo ORM starter template with:

- Piccolo models in `tables.py`
- Auto CRUD API via `piccolo_api`
- Piccolo admin mounted at `/admin`
- Session auth endpoints

## Quick start

```bash
python -m pip install -r requirements.txt
python -m uvicorn app:app --reload
```

## Bootstrap admin user

Create your first admin account for the Piccolo admin panel:

```bash
python create_superuser.py
```

If the username already exists, the script updates that user and ensures admin / superuser access is enabled.

Open:

- `http://localhost:8000/docs`
- `http://localhost:8000/admin`

## Core idea

Edit `tables.py` and your storage schema, admin surface, and API resources evolve with the model.


## GitHub Codespaces Setup

GitHub Codespaces is a flexible cloud-based development environment. Your editor runs in the cloud, allowing you to work from anywhere.

## Creating and Starting a Codespace

### Create a New Codespace

1. **Go to your Repository**
   - Navigate to your **python-flask-todo**

2. **Create a Codespace**
   - Click the green **"Code"** button
   - Select the **"Codespaces"** tab
   - Click **"Create codespace on main"** (or your preferred branch)

3. **Wait for Setup**
   - GitHub will provision your Codespace (this takes 1-2 minutes)
   - VS Code will open in your browser automatically
   - The environment is ready when you see the terminal

### Start an Existing Codespace

If you've created a Codespace before:

1. **Go to Your Codespaces**
   - Visit [https://github.com/codespaces](https://github.com/codespaces)
   - Click on your Codespace name to open it

2. **Or via GitHub**
   - Click the green **"Code"** button on the repository
   - Select the **"Codespaces"** tab
   - Click on an existing Codespace to resume it

## Install Dependencies

```bash
py -m pip install -r requirements.txt
```

## Important: Codespaces Port Configuration

If you're running in **GitHub Codespaces**, you must set the forwarded port to **Public** for Auth0 callbacks to work:

1. Open the **Ports** panel (bottom of VS Code)
2. Right-click the port 5000
3. Select "Port Visibility" → **Public**

