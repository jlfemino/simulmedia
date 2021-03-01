import configparser
from pathlib import Path

config_parser = configparser.ConfigParser()
config_filepath = f'{Path(__file__).parent.parent.parent}/config.ini'
config_parser.read(config_filepath)
