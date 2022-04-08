from rich_click import command as rich_command
from rich_click import group as rich_group
from rich_click import RichCommand
from rich_click import RichGroup

import click

click.group = rich_group
click.command = rich_command
click.Command = RichCommand
click.Group = RichGroup

from app.cli import cli

cli()
