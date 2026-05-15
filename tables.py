from piccolo.columns import Boolean, ForeignKey, Varchar, Text, Integer, Float, Timestamptz
from piccolo.columns.readable import Readable
from piccolo.columns.defaults.timestamptz import TimestamptzNow
from piccolo.table import Table
from piccolo.apps.user.tables import BaseUser
from piccolo_api.session_auth.tables import SessionsBase


class Category(Table):
    name = Varchar(length=50, required=True, unique=True)

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.name])


class Todo(Table):
    task = Varchar(length=200, required=True)
    user = ForeignKey(references=BaseUser, null=False)
    category = ForeignKey(references=Category, null=False, help_text="Select a category")
    created = Timestamptz(default=TimestamptzNow())
    done = Boolean(default=False)

async def initialize_schema_and_seed() -> None:
    # Create User & Session Tables
    await BaseUser.create_table(if_not_exists=True)
    await SessionsBase.create_table(if_not_exists=True)
    from app_startup import ensure_env_superuser
    await ensure_env_superuser()

    # Create App Tables
    await Category.create_table(if_not_exists=True)
    await Todo.create_table(if_not_exists=True)

    # Create Default Categories 
    if not await Category.exists().where(Category.name == "Urgent"):
        await Category(name="Urgent").save()

    if not await Category.exists().where(Category.name == "Non-urgent"):
        await Category(name="Non-urgent").save()
