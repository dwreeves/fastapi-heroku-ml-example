import asyncio

import click
from celery.bin.celery import celery as celery_cmd
from click_didyoumean import DYMGroup


@click.group("app", cls=DYMGroup)
def cli():
    pass


cli: click.Group


@cli.command("seed-db")
def seed_db_command():
    """Add data to the airports table."""
    click.echo("Seeding database...")
    from app.db.process import seed_db
    asyncio.run(seed_db())
    click.echo("Database has been seeded.")


seed_db_command: click.Command


# load the Celery app to assist the Celery CLI.
import app.celery  # noqa: F401, E402

cli.add_command(celery_cmd)
