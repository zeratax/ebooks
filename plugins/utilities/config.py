import json
import os


def set_config(config_file):
    global c
    c = Configuration(config_file)


def load_config(file):
    with open(file) as f:
        return json.load(f)


class Configuration:
    def __init__(self, file):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../../"
        try:
            self.config = load_config(ROOT_DIR + file)
            self.bot_c = self.config['bot']
            self.plugin_c = self.config['plugins']
        except NameError:
            print("no config given")
