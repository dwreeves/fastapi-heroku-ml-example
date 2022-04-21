import asyncio

import click
from celery.bin.celery import celery as celery_cmd
from click_didyoumean import DYMGroup

from app.config import settings


@click.group("app", cls=DYMGroup)
def cli():
    pass


cli: click.Group


@cli.command("seed-db")
@click.option("--filename", "-f",
              help=f"Name of a data file in {settings.DEFAULT_STATIC_DATA_DIR}")
def seed_db_command(filename: str = None):
    """Add data to the airports table."""
    click.echo("Seeding database...")

    if filename is None:
        path = settings.DEFAULT_AIRPORTS_CSV_FULL_PATH
    else:
        path = settings.DEFAULT_STATIC_DATA_DIR / filename

    from app.db.process import seed_db
    asyncio.run(seed_db(path=path))

    click.echo("Database has been seeded.")


seed_db_command: click.Command


# load the Celery app to assist the Celery CLI.
import app.celery  # noqa: F401, E402


cli.add_command(celery_cmd)
