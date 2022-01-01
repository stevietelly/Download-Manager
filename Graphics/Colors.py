import importlib
import Assets.Functions.Parser as p


def get_main_theme_color(essence="tuple"):
    importlib.reload(p)
    if essence == "tuple":
        if p.KeyMatch().match("theme") == "Pink-lady":
            color = (1, .4, .5, 1)  # FF6680
            return color

        elif p.KeyMatch().match("theme") == "Ocean_Blue":
            color = (.16, .55, 1, 1)
            return color

        elif p.KeyMatch().match("theme") == "Dark":
            color = (.3, .3, .3, 1)
            return color
    elif essence == "string":
        if p.KeyMatch().match("theme") == "Pink-lady":
            color = "#FF6680"
            return color

        elif p.KeyMatch().match("theme") == "Ocean_Blue":
            color = "#298CFF"
            return color

        elif p.KeyMatch().match("theme") == "Dark":
            color = "#505050"
            return color


def get_sub_theme_color(essence="tuple"):
    importlib.reload(p)
    if essence == "tuple":
        if p.KeyMatch().match("theme") == "Pink-lady":
            color = (1, .5, .55, .7)
            return color

        elif p.KeyMatch().match("theme") == "Ocean_Blue":
            color = (.19, .65, .9, .7)
            return color

        elif p.KeyMatch().match("theme") == "Dark":
            color = (.5, .5, .5, .7)
            return color
    elif essence == "string":
        if p.KeyMatch().match("theme") == "Pink-lady":
            color = "#FF808C"
            return color

        elif p.KeyMatch().match("theme") == "Ocean_Blue":
            color = "#298CFF"
            return color

        elif p.KeyMatch().match("theme") == "Dark":
            color = "#505050"
            return color


def get_transparent_sub_theme_color(essence="tuple"):
    importlib.reload(p)
    if essence == "string":
        if p.KeyMatch().match("theme") == "Pink-lady":
            color = "#FF9BA0"
            return color

        elif p.KeyMatch().match("theme") == "Ocean_Blue":
            color = "#6AAFFF"
            return color

        elif p.KeyMatch().match("theme") == "Dark":
            color = "8F8D8A"
            return color
    elif essence == "tuple":
        if p.KeyMatch().match("theme") == "Pink-lady":
            color = (1, .6, .62, 1)
            return color

        elif p.KeyMatch().match("theme") == "Ocean_Blue":
            color = (.41, .68, 1, 1)
            return color

        elif p.KeyMatch().match("theme") == "Dark":
            color = (.56, .55, .54, 1)
            return color
