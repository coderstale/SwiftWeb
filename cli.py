import click
from my_framework.server import run as run_server
from logging_config import logger


@click.group()
def cli():
    pass


@cli.command()
@click.option('--port', default=8000, help='Port to run the server on.')
def runserver(port):
    logger.info(f"Starting server on port {port}")
    run_server(port=port)


if __name__ == '__main__':
    cli()

