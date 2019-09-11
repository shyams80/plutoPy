import configparser
import os

path = os.path.join(os.environ.get('PLUTO_PY_CONFIG_PATH', ''), 'config.ini')

config = configparser.ConfigParser()
config.read(path)
