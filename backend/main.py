#!/usr/bin/env python3

# Copyright (c) 2014-2021, Linus Östberg and contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of kimenu nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
Main script for choosing what restaurant parsers to use.
"""

import json
import os
import re
import sys
from datetime import date, datetime, tzinfo
import pytz
import locale
import parser as ps
from time import timezone

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
REST_FILENAME = os.path.join(__location__, "restaurants.json")


def read_restaurants(intext: str) -> dict:
    """
    Parse the list of restaurants from the restaurants file.

    Args:
        intext(str): The text loaded from the restaurants file.
    """
    indata = json.loads(intext)
    data = dict()
    for entry in indata["restaurants"]:
        data[entry["identifier"]] = entry
    return data

REST_DATA = read_restaurants(open(REST_FILENAME).read())

# works as ordered dict as well, but must be _ordered_
MAPPER = {
    "jorpes": ps.parse_jorpes,
    "glada": ps.parse_glada,
    "haga": ps.parse_haga,
    "hjulet": ps.parse_hjulet,
    "jons": ps.parse_jons,
    "livet": ps.parse_livet,
    "nanna": ps.parse_nanna,
    "svarta": ps.parse_svarta,
    "bikupan": ps.parse_bikupan,
    "dufva": ps.parse_dufva,
    "hubben": ps.parse_hubben,
    "rudbeck": ps.parse_rudbeck,
    "tallrik": ps.parse_tallrik,
    "nordicforum": ps.parse_nordicforum,
    "tastorykista": ps.parse_tastorykista,
    "glaze": ps.parse_glaze

}


KI = ("jorpes", "glada", "haga", "hjulet", "jons", "livet", "nanna", "svarta")

UU = ("bikupan", "dufva", "hubben", "rudbeck", "tallrik")

KA = ("uppereast", "nordicforum", "tastorykista", "eaterygate", "eaterynod", "wildkitchen", "glaze")


def activate_parsers(restaurants, restaurant_data):
    """
    Run the wanted parsers
    """
    output = []
    for restaurant in restaurants:
        if ".kvartersmenyn.se" in restaurant_data[restaurant]["menuUrl"]:
            MAPPER[restaurant] = ps.parse_kvartersmenyn
        data = MAPPER[restaurant](restaurant_data[restaurant])
        output.append(f"""<div class="title">\n\t<a class="gmaps" href="{data['map_url']}"></a>""")
        output.append(
            f"""\t<a href="{data['url']}">{data['title']}</a></div>"""
        )
        if "menu" in data:
            output.append('<div class="menu">')
            output.append("<p>")
            output.append("<br />\n".join(data["menu"]))
            output.append("</p>")
        output.append("</div>")
    return "\n".join(output)


def get_restaurant(name: str) -> dict:
    """
    Request the menu of a restaurant
    """
    if name in MAPPER:
        return MAPPER[name](REST_DATA[name])
    else:
        return {}


def list_restaurants():
    """
    List all supported restaurants.
    """
    return list(REST_DATA.values())


def page_end():
    """
    Print the closure of tags etc
    """

    lines = list()
    lines.append("</div>")
    lines.append(
        '<div class="updated">'+
        datetime.now(pytz.timezone("Europe/Stockholm")).strftime("%Y-%m-%d %H:%M:%S") +
        '</div>'
    )
    lines.append('<div class="footer">')
    lines.append('<a id="copy_button" href="#" onclick="copyToClipboard(); return false;">Copy</a>')
    lines.append('<a href="https://github.com/frias0/lunch-menu/issues/new?assignees=&labels=enhancement&template=request-restaurant.md&title=%5BRESTAURANT%5D+Adding+X">Add restaurant</a>')
    lines.append('</div>')
    lines.append("</body>")
    lines.append("</html>")
    return lines


def page_start(weekday, day, month):
    """
    Print the initialisation of the page
    """
    lines = list()
    lines.append("<html>")
    lines.append("<head>")
    date = weekday.capitalize() + " " + str(day) + " " + str(month)
    lines.append("<title>Dagens mat - {}</title>".format(date))
    lines.append('<link href="styles.css" rel="stylesheet" type="text/css">')
    lines.append('<style type="text/css"></style>')
    lines.append('<script src="js.js"></script>')
    lines.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    lines.append('<meta name="color-scheme" content="dark light">')
    lines.append('<link rel="icon" href="favicon.svg" type="image/svg+xml">')
    lines.append("</head>")
    lines.append("<body>")
    lines.append('<p class="warning"> Information is stale</p>')
    lines.append('<div id="content">')

    # page formatting
    lines.append("")
    return lines


def parse_restaurant_names(rest_names):
    """
    Decide what restaurants to generate menus for
    """
    restaurants = list()
    for param in rest_names:
        if param not in KI and param not in UU and param not in KA:
            raise ValueError("{} not a valid restaurant".format(param))
        restaurants.append(param.lower())
    return restaurants


def print_usage(supported):
    """
    Print description of syntax
    """
    sys.stderr.write("Usage: {} restaurant1 [...] \n".format(sys.argv[0]))
    sys.stderr.write("Supported restaurants: {}\n".format(", ".join(sorted(supported))))
    sys.stderr.write("Write all to generate all supported restaurants\n")


def gen_ki_menu():
    """
    Generate a menu for restaurants at KI
    """
    output = ""
    output += "\n".join(page_start(ps.get_weekday(), str(ps.get_day()), ps.get_month()))
    output += activate_parsers(KI, REST_DATA)
    output += "\n".join(page_end())
    return output


def gen_uu_menu():
    """
    Generate a menu for restaurants at UU
    """
    output = ""
    output += "\n".join(page_start(ps.get_weekday(), str(ps.get_day()), ps.get_month()))
    output += activate_parsers(UU, REST_DATA)
    output += "\n".join(page_end())

    sys.stderr.write(output + "\n")
    return output

def gen_kista_menu():
    """
    Generate a menu for restaurants at KISTA
    """
    output = ""
    output += "\n".join(page_start(ps.get_weekday(), str(ps.get_day()), ps.get_month()))
    output += activate_parsers(KA, REST_DATA)
    output += "\n".join(page_end())

    sys.stderr.write(output + "\n")
    return output


if __name__ == "__main__":
    if len(sys.argv) < 2 or "-h" in sys.argv:
        print_usage(KI + UU + KA)
        sys.exit()

    REST_NAMES_IN = tuple()
    if "all" in sys.argv[1:]:
        REST_NAMES_IN += KI + UU + KA
    elif "ki" in sys.argv[1:]:
        REST_NAMES_IN += KI
    elif "uu" in sys.argv[1:]:
        REST_NAMES_IN += UU
    elif "ka" in sys.argv[1:]:
        REST_NAMES_IN += KA
    else:
        REST_NAMES_IN = [param for param in sys.argv[1:] if param != "-r"]

    try:
        REST_NAMES = parse_restaurant_names(REST_NAMES_IN)
    except ValueError as err:
        sys.stderr.write("E: {}\n".format(err))
        print_usage((x for x in MAPPER))
        sys.exit(1)

    # print the menus
    print("\n".join(page_start(ps.get_weekday(), str(ps.get_day()), ps.get_month())))
    print(activate_parsers(REST_NAMES, REST_DATA))
    print("\n".join(page_end()))
