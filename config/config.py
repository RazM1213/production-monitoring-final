import yaml
from yaml import Loader

from consts.paths import ABSOLUTE_PATH_YAML

with open(ABSOLUTE_PATH_YAML, "r") as yaml_file:
    CONFIG = yaml.load(yaml_file, Loader=Loader)

ENV_NAME = CONFIG["env"]["env_name"]
TOPIC = CONFIG["kafka"]["topic"]
BOOTSTRAP_SERVERS = CONFIG["kafka"]["bootstrap_servers"]
BASE_URL = CONFIG["url"]["base_url"]
ROUTE_1 = CONFIG["url"]["route_1"]
ROUTE_2 = CONFIG["url"]["route_2"]
POST_REQUEST_BODY = CONFIG["request_body"]["post"]
