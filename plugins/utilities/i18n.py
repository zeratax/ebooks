from plugins.utilities import commands

import json
import os

directory = "plugins/utilities/i18n"
settings = {}
logger = commands.logger

if not os.path.isdir(directory):
    os.makedirs(directory)
elif os.path.isfile(directory + "/settings.json"):
    try:
        with open(directory + "/settings.json") as f:
            settings = json.load(f)
    except ValueError:
        logger.error("i18n settings json corrupted!")
        copyfile(directory + "/settings.json", directory + "/settings.corrupt")


def loc(server_id, plugin, str):
    if server_id not in settings:
        settings[server_id] = "english"
    language = settings[server_id]
    try:
        with open("{}/{}.json".format(directory, plugin)) as f:
            translation = json.load(f)
            try:
                return translation[language][str]
            except KeyError:
                logger.warning("no translation for {}:{} in {}".format(
                    plugin, str, language))
                return translation["english"][str]
    except ValueError:
        logger.error("{}/{}.json is corrupted".format(directory, plugin))
    except IOError:
        logger.error("{}/{}.json does not exist".format(directory, plugin))


def set_language(server_id, language):
    settings[server_id] = language
    with open(directory + "/settings.json", 'w') as f:
        json.dump(settings, f)
