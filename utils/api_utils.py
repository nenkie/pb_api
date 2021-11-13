import json
import os.path as p


def load_config_file(config_file, config_section=None):
    if not p.isfile(config_file):
        raise FileNotFoundError

    with open(config_file, "r") as f:
        content = json.loads(f.read())

    if config_section:
        return content[config_section]

    return content
