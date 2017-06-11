###
# This plugin includes math related commands.
###
from plugins.utilities import commands
from plugins.utilities import config
from plugins.utilities import formatter
from plugins.utilities import i18n

from sympy import *
import hashlib
import os
import re

x, y, z, t = symbols("x y z t")
directory = "plugins/maths/output/"
LATEX_TEMPLATE = directory + "../template.tex"
bg = "36393E"
fg = "DBDBDB"
dpi = 400


def initialize_commands():
    global logger
    global conf
    global LATEX_TEMPLATE
    global bg
    global fg
    global dpi

    logger = commands.logger

    try:
        conf = config.c.plugin_c['maths']
    except NameError:
        logger.warning("config is missing settings for the maths module")

    LATEX_TEMPLATE = directory + "../" + conf["latex_template"]
    bg = conf["backgroundcolour"]
    fg = conf["foregroundcolour"]
    dpi = conf["dpi"]

    if not os.path.isdir(directory):
        os.makedirs(directory)

    commands.create_command("maths",
                            "sympyfy",
                            ["sympyfy", "calculate", "calc", "simplify"],
                            "Simplifies a mathematical expression")

    commands.create_command("maths",
                            "render_latex",
                            ["render"],
                            "renders latex expressions with pdflatex")


def make_simple(expr, output):
    try:

        expr_simply = simplify(expr)
        if output == "latex" or output == "tex":
            expr_simply = "$" + latex(expr_simply) + "$"
        elif output == "ascii" or output == "unicode":
            expr_simply = pretty(expr_simply)
        return str(expr_simply)
    except SympifyError:
        return "Could not parse " + str(expr)


async def sympyfy(client, message):
    expr = commands.remove_keywords(client, message.content, "maths", "sympyfy")
    expr = re.sub("\s+", " ", expr).strip()
    if message.server:
        server_id = message.server.id
    else:
        server_id = message.author.id
    if expr == "":
        await client.send_message(message.channel,
                                  formatter.warning(i18n.loc(server_id,
                                                           "maths",
                                                           "empty_expr_sym")))
    else:
        await client.send_typing(message.channel)
        msg = await client.send_message(message.channel,
                                        formatter.processing(i18n.loc(server_id,
                                                                 "maths",
                                                                 "processing")))
        output_formats = ["latex", "tex", "unicode", "ascii"]
        for format in output_formats:
            if format in expr:
                expr = expr.replace(format, "")
                await client.edit_message(msg, "```{}```".format(make_simple(expr, format)))
                return
        await client.edit_message(msg, "`{}`".format(make_simple(expr, False)))


def cleanup_output_files(hash):
    try:
        os.remove(directory + hash + ".tex")
        os.remove(directory + hash + ".dvi")
        os.remove(directory + hash + ".aux")
        os.remove(directory + hash + ".log")
    except OSError:
        pass


def generate_image(latex):
    hash = hashlib.md5(latex.encode("utf-8")).hexdigest()
    latex_file = directory + hash + ".tex"
    dvi_file = directory + hash + ".dvi"
    png_file = directory + hash + ".png"

    if os.path.isfile(png_file):
        return png_file
    else:
        with open(LATEX_TEMPLATE, "r") as textemplatefile:
            textemplate = textemplatefile.read()

            with open(latex_file, "w") as tex:
                backgroundcolour = bg
                textcolour = fg
                latex = textemplate.replace("__DATA__", latex).replace(
                    "__BGCOLOUR__", backgroundcolour).replace("__TEXTCOLOUR__",
                                                              textcolour)

                tex.write(latex)
                tex.flush()
                tex.close()

        imagedpi = dpi
        try:
            latexsuccess = os.system(
                "pdflatex -output-directory={} {}".format(directory[:-1],
                                                          latex_file))
        except Exception:
            pass
        if latexsuccess == 0:
            os.system(
                "dvipng -T tight -D {} {} -o {}".format(imagedpi, dvi_file,
                                                        png_file))
            cleanup_output_files(hash)
            return png_file
        else:
            cleanup_output_files(hash)
            return ""


async def render_latex(client, message):
    expr = commands.remove_keywords(client, message.content, "maths",
                                    "render_latex")
    expr = re.sub("\s+", " ", expr).strip()
    if message.server:
        server_id = message.server.id
    else:
        server_id = message.author.id
    if expr == "":
        await client.send_message(message.channel,
                                  formatter.warning(i18n.loc(server_id,
                                                           "maths",
                                                           "empty_expr_tex")))
    else:
        await client.send_typing(message.channel)
        image = generate_image(expr)
        if os.path.isfile(image):
            with open(image, "rb") as f:
                await client.send_file(message.channel, f)
        else:
            await client.send_message(message.channel,
                                      formatter.error(i18n.loc(server_id,
                                                               "maths",
                                                               "err_rendering")))
