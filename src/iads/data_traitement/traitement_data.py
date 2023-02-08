import re
import numpy as np


def update_title_jeux(arr):
    title = arr["titre"]
    title = re.sub(
        r'https://www.trictrac.net/jeu-de-societe/(.*)/?.*', r'\1', arr["url"])
    return title


def parse_casting(castings):
    castings = str(castings)
    castings = re.sub(r'(.*) De (.*)', r'\1 Par \2', castings)
    castings = re.sub(r'(Par|Illustré|Édité|Distribué|De)', r'\n\1', castings)

    castings = castings.split("\n")

    if "" in castings:
        castings.remove("")

    return castings


def extract_creators(arr):
    castings = parse_casting(arr["casting"])
    creators = np.NaN

    for cas in castings:
        if cas.startswith("Par"):
            creators = cas.replace("Par ", "")
            return creators

        if cas.startswith("De"):
            creators = cas.replace("De ", "")
            return creators

    return creators


def extract_illustrators(arr):
    castings = parse_casting(arr["casting"])
    illustrators = np.NaN

    for cas in castings:
        if cas.startswith("Illustré"):
            illustrators = cas.replace("Illustré par ", "")
            return illustrators

    return illustrators


def extract_editors(arr):
    castings = parse_casting(arr["casting"])
    editors = np.NaN

    for cas in castings:
        if cas.startswith("Édité"):
            editors = cas.replace("Édité par ", "")
            return editors

    return editors


def extract_distributors(arr):

    castings = parse_casting(arr["casting"])
    distributors = np.NaN

    for cas in castings:
        if cas.startswith("Distribué"):
            distributors = cas.replace("Distribué par ", "")
            return distributors

    return distributors
