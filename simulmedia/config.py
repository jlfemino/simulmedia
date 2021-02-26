import configparser
from pathlib import Path

# Config object
config_parser = configparser.ConfigParser()
config_filepath = f'{Path(__file__).parent.parent}/config.ini'
config_parser.read(config_filepath)

config = config_parser['DEFAULT']
