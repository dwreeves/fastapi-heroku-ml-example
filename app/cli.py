import asyncio

import click
from celery.bin.celery import celery as celery_cmd


@click.group("app")
def cli():
    pass


cli: click.Group


@cli.command("seed-db")
def seed_db_command():
    """Add data to the airports table."""
    from app.db.process import seed_db
    asyncio.run(seed_db())


seed_db_command: click.Command


# load the Celery app to assist the Celery CLI.
import app.celery  # noqa: E402, F401

cli.add_command(celery_cmd)
