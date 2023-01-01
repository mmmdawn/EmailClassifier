import click

from cli.train import train
from cli.server import start_server


@click.group()
@click.version_option(version='1.6.3')
@click.pass_context
def cli(ctx):
    pass


cli.add_command(train, "train")
cli.add_command(start_server, "start_server")
