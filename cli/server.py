import threading
import click
import uvicorn
import webbrowser
from api import app


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
def start_server():
    threading.Thread(target=run_server).start()
    threading.Thread(target=open_browser).start()


def open_browser():
    webbrowser.open("http://localhost:8000/static/index.html")


def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
