# flake8: noqa: #402
import click
from rich_click import command as rich_command
from rich_click import group as rich_group
from rich_click import RichCommand
from rich_click import RichGroup


click.group = rich_group
click.command = rich_command
click.Command = RichCommand
click.Group = RichGroup

from app.cli import cli


cli()
