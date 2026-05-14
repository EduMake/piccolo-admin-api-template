import os

from piccolo.apps.user.tables import BaseUser

from tables import Category, Todo


async def ensure_env_superuser() -> None:
    admin_username = (os.getenv("ADMIN_USERNAME") or "").strip()
    admin_password = os.getenv("ADMIN_PASSWORD") or ""
    admin_email = (os.getenv("ADMIN_EMAIL") or "").strip() or None

    superuser_exists = await BaseUser.exists().where(BaseUser.superuser == True)
    if superuser_exists:
        return

    if not admin_username or not admin_password:
        print(
            "No superuser exists. Set ADMIN_USERNAME and ADMIN_PASSWORD to bootstrap one at startup."
        )
        return

    await BaseUser.create_user(
        username=admin_username,
        password=admin_password,
        email=admin_email,
        admin=True,
        superuser=True,
        active=True,
    )
    print(f"Bootstrapped superuser '{admin_username}' from environment variables.")
