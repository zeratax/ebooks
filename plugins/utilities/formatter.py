import asyncio
import math
import string


class PluralDict(dict):
    def  __missing__(self, key):
        if ",plural," in key:
            key, rest = key.split(',plural,', 1)
            value = super().__getitem__(key)
            # print("value: " + str(value))
            # print("key: " + str(key))
            if isinstance(value, (list, tuple)):
                value = len(value)
            suffix = rest.split(',')
            # print("value: " + str(value))
            # print("suffix: " + str(suffix))
            # print("----------------------")
            if len(suffix) == 1:
                return "" if value <= 1 else suffix[0]
            if len(suffix) == 2:
                return suffix[0] if value <= 1 else suffix[1]
            if len(suffix) == 3:
                if value == 0:
                    return suffix[0]
                elif value == 1:
                    return suffix[1]
                elif value >= 2:
                    return suffix[2]
        elif ",lst" in key:
            key, rest = key.split(',lst', 1)
            value = super().__getitem__(key)
            value = str(value).strip('[]').replace("'","")
            return value
        else:
            raise KeyError(key)


def warning(message):
    message = ":x:" + message
    return message


def error(message):
    message = ":exclamation: " + message
    return message


def processing(message):
    message = ":gear: " + message
    return message


def success(message):
    message = ":white_check_mark: " + message
    return message


def win(message):
    message = ":trophy::trophy::trophy: **" + message.strip() + \
              "** :trophy::trophy::trophy:"
    return message


def lost(message):
    message = ":weary: " + message
    return message


def link(message):
    message = ":link: " + message
    return message


def person(message):
    message = ":bust_in_silhouette: " + message
    return message


async def wrap_message(client, destination, string):
    length = len(string)
    if(length > 1999):
        for i in range(math.ceil(length / 2000)):
            await client.send_message(destination,
                                      string[2000 * i:2000 * (i + 1)])
            await asyncio.sleep(1)
