###
# This plugin  is used for not safe for work content
###
from plugins.utilities import commands
from plugins.utilities import formatter
from plugins.utilities import i18n

import discord

import datetime
import json
import re
import requests
from bs4 import BeautifulSoup

brackets = re.compile(r"(?:\(|\[|\{)[^(?:\)|\]|\})]*(?:\)|\]|\})")
sadpanda_link = re.compile(
    r"(?i)https?:\/\/(?:www\.)?(?:ex|e-)hentai.org\/g\/(\S+)\/(\S+)\/")
fakku_link = re.compile(
    r"(?i)https:\/\/(?:www\.)fakku\.net\/(?:hentai|manga)\/(\S*)")
pururin_link = re.compile(
    r"(?i)https?:\/\/(?:www\.)?pururin.us\/gallery\/\d+\/\S+")


def initialize_commands():
    commands.create_command("nsfw",
                            "doujin_info",
                            ["fakku.net", "exhentai.org", "e-hentai.org",
                             "pururin.us"],
                            "Shows info about the linked gallery",
                            mention=False)


def gallery_preview(website, gallery, server_id):
    artists, male_tags, female_tags, misc_tags, parodies, groups, characters, languages = (
        [] for i in range(8))

    if website == "Fakku":
        title = gallery["content_name"]

        category = ["content_category"]

        date = datetime.datetime.fromtimestamp(
            int(gallery["content_date"])
        ).strftime("%Y-%m-%d %H:%M")

        rating = i18n.loc(server_id, "nsfw", "rating_fakku").format(
            gallery["content_favorites"])

        for tag in gallery["content_tags"]:
            misc.append(tag["attribute"])

        for artist in gallery["content_artists"]:
            artists.append(artist["attribute"])

        for serie in gallery["content_series"]:
            parody_tag.append(serie["attribute"])

        if "content_description" in gallery:
            description = gallery["content_description"]
        else:
            description = "/"
        thumbnail = ""
    elif website == "sadpanda":
        title_eng = re.sub(brackets, "",
                           re.sub(brackets, "", gallery["title"])).strip()
        title_jpn = re.sub(brackets, "",
                           re.sub(brackets, "", gallery["title_jpn"])).strip()
        if title_jpn != title_eng and title_jpn != "":
            title = title_jpn + " **/** " + title_eng
        else:
            title = title_eng

        category = gallery["category"]

        uploader = gallery["uploader"]

        pages = int(gallery["filecount"])

        date = datetime.datetime.fromtimestamp(
            int(gallery["posted"])
        ).strftime("%Y-%m-%d %H:%M")

        for tag in gallery["tags"]:
            if "artist:" in tag:
                artists.append(tag[7:])
            elif "female:" in tag:
                female_tags.append(tag[7:])
            elif "male:" in tag:
                male_tags.append(tag[5:])
            elif "parody:" in tag:
                parodies.append(tag[7:])
            elif "group:" in tag:
                groups.append(tag[6:])
            elif "character:" in tag:
                characters.append(tag[10:])
            elif "language:" in tag:
                languages.append(tag[9:])
            else:
                misc_tags.append(tag)

        thumbnail = gallery["thumb"]

        rating = i18n.loc(server_id, "nsfw", "rating_sadpanda")
        for i in range(round(float(gallery["rating"]))):
            rating += ":star:"
        rating += "({})".format(float(gallery["rating"]))

    elif website == "pururin":
        date = "/"
        thumbnail = ""
        pages = int(gallery["Pages"].split(" ")[0])
        title = gallery["title"].replace("|", "**/**")
        artists = gallery["Artist"]
        misc_tags = gallery["Contents"]
        parodies = gallery["Parody"]
        groups = gallery["Circle"]
        characters = gallery["Character"]
        languages = gallery["Language"]
        category = gallery["Category"][0]
        uploader = gallery["Uploader"]

        rating = i18n.loc(server_id, "nsfw", "rating_sadpanda")
        for i in range(int(gallery["Ratings"])):
            rating += ":star:"
        rating += "({})".format(gallery["Ratings"])

    data = {"title": title, "category": category, "languages": languages,
            "artists": artists, "groups": groups, "pages": pages, "uploader":uploader, "date": date,
            "rating": rating, "parodies": parodies, "characters": characters,
            "female_tags": female_tags, "male_tags": male_tags,
            "misc_tags": misc_tags, "thumbnail": thumbnail}

    preview = i18n.loc(server_id, "nsfw", "preview").format_map(
        formatter.PluralDict(data))
    return preview


def match_class(target):
    def do_match(tag):
        classes = tag.get('class', [])
        return all(c in classes for c in target)
    return do_match


def pururin_parser(html_doc):
    gallery = {}
    soup = BeautifulSoup(html_doc, 'html.parser')
    for row in soup.table.find_all('tr'):
        if row.td.string not in gallery:
            gallery[row.td.string] = []
        if row.ul:
            if row.ul.string != "":
                for elements in row.ul.find_all('a'):
                    gallery[row.td.string].append(elements.string)
        elif row.a:
            gallery[row.td.string] = row.a.string.strip()
        elif row.span:
            gallery[row.td.string] = float(row.find(match_class(["full"]))['data-star'])
            if row.find(match_class(["half"])):
                gallery[row.td.string] += 0.5
        elif row.td:
            gallery[row.td.string] = row.find_all('td')[1].string
    title = soup.find(match_class(["title"])).string
    gallery["title"] = title
    return gallery


async def doujin_info(client, message):
    sadpanda_galleries = re.findall(sadpanda_link, message.content)
    fakku_galleries = re.findall(fakku_link, message.content)
    pururin_galleries = re.findall(pururin_link, message.content)
    if message.server:
        server_id = message.server.id
    else:
        server_id = message.author.id
    if sadpanda_galleries:
        await client.send_typing(message.channel)
        payload = json.loads(
            '{"method" : "gdata", "gidlist" : [], "namespace": 1 }')
        for gallery in sadpanda_galleries:
            gid = int(gallery[0])
            gt = gallery[1]
            payload["gidlist"].append([gid, gt])
        url = "https://e-hentai.org/api.php"
        header = {"Content-type": "application/json"}
        sadpanda_response = requests.post(url, data=json.dumps(payload),
                                          headers=header)
        if sadpanda_response.status_code == 200:
            for gallery_dict in sadpanda_response.json()["gmetadata"]:
                await client.send_message(message.channel,
                                          gallery_preview("sadpanda",
                                                                gallery_dict,
                                                                server_id))
        else:
            await client.send_message(message.channel,
                                      formatter.error(i18n.loc(server_id,
                                                               "nsfw",
                                                               "api_dead")))
    if fakku_galleries:
        await client.send_typing(message.channel)
        for gallery in fakku_galleries:
            api_url = "https://api.fakku.net/manga/" + gallery
            try:
                gallery_dict = requests.get(api_url).json()["content"]
                await client.send_message(message.channel,
                                          gallery_preview("fakku",
                                                          gallery_dict,
                                                          server_id))
            except json.decoder.JSONDecodeError:
                await client.send_message(message.channel,
                                          formatter.error(i18n.loc(server_id,
                                                                   "nsfw",
                                                                   "api_dead")))
    if pururin_galleries:
        await client.send_typing(message.channel)
        for gallery in pururin_galleries:
            try:
                html = requests.get(gallery).text
                gallery_dict = pururin_parser(html)
                await client.send_message(message.channel,
                                          gallery_preview("pururin",
                                                          gallery_dict,
                                                          server_id))
            except requests.ConnectionError:
                await client.send_message(message.channel,
                                          formatter.error(i18n.loc(server_id,
                                                                   "nsfw",
                                                                   "api_dead")))
