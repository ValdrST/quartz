import json
import sys
import os.path

import click

from quartz.service import EventerService
from quartz.models import set_db_parameters
from quartz import __version__

BANNER = """
                                 _
          __ _ _   _  __ _ _ __| |_ ____
         / _` | | | |/ _` | '__| __|_  /
        | (_| | |_| | (_| | |  | |_ / /
         \__, |\__,_|\__,_|_|   \__/___|
            |_|

    Current version: {version}
""".format(version=__version__)

DEFAULTS = {
    "database_url": "mongo://localhost:27017/eventer",
    "host": "0.0.0.0",
    "port": 8000,
    "registry": []
}


def get_config_value(config, key):
    return config.get(key, DEFAULTS[key])


def print_banner(config_file):
    print(BANNER)
    print("")
    print("Using the configuration file '{0}'".format(os.path.abspath(config_file)))
    print("")


@click.group()
def cli():
    pass


@cli.command("start", help="The JSON configuration file with the parameters")
@click.argument("config")
def start(config):
    print_banner(config)
    with open(config) as f:
        cfg = json.load(f)
    set_db_parameters(get_config_value(cfg, "database_url"))
    service = EventerService(get_config_value(cfg, "host"), get_config_value(cfg, "port"),
                             get_config_value(cfg, "registry"))
    service.start()


SAMPLE_CONFIG = """{
    "database_url": "mongo://localhost:27017/eventer",

    "host": "127.0.0.1",
    "port": 8000,

    "registry": []
}"""


@cli.command("init", help="Writes a sample configuration file to STDOUT. Can be used as template"
                          " for writing the actual configration file")
def init():
    print(SAMPLE_CONFIG)
