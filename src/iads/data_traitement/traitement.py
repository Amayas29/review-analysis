import re
import numpy as np


def update_title(arr):
    try:
        _ = arr["title"]
        return re.sub(r'https://www.trictrac.net/jeu-de-societe/(.*)/.*', r'\1', arr["url"])
    except Exception:
        return re.sub(r'https://www.trictrac.net/jeu-de-societe/(.*)', r'\1', arr["url"])


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


def extract_published_year(arr):
    match = re.search(r"\b\d{4}\b", arr["date_published"])

    if match:
        year = match.group()
        return year

    return np.NaN


def parse_gameplay(gameplay):
    return gameplay.split("|")


def extract_players(arr):
    nb_players = parse_gameplay(arr["gameplay"])[0]
    min_p = 1
    max_p = 99

    if nb_players.startswith("jusqu'à"):
        nb_players = nb_players.replace("jusqu'à ", "")
        max_p = int(nb_players)

    elif nb_players.startswith("à partir de"):
        nb_players = nb_players.replace("à partir de ", "")
        min_p = int(nb_players)

    elif "à" in nb_players:
        nb_players = nb_players.split("à")
        min_p = int(nb_players[0])
        max_p = int(nb_players[1])

    else:
        try:
            min_p = int(nb_players)
            max_p = min_p
        except ValueError:
            return np.NaN

    return f"{min_p}-{max_p}"


def extract_ages(arr):
    age = parse_gameplay(arr["gameplay"])[1]
    age = age.replace("\xa0", "")

    min_a = 1
    max_a = 99

    if age.startswith("jusqu'à"):
        age = age.replace("jusqu'à ", "")
        max_a = int(age)

    elif "ans et +" in age:
        age = age.replace("ans et +", "")
        min_a = int(age)

    elif "à" in age:
        age = age.split("à")
        min_a = int(age[0])
        max_a = int(age[1])

    else:
        try:
            min_a = int(age)
            max_a = min_a
        except ValueError:
            return np.NaN

    return f"{min_a}-{max_a}"


def extract_duration(arr):
    duration = parse_gameplay(arr["gameplay"])[2]
    duration = duration.replace("\xa0", "")

    try:
        durr = int(duration)
    except ValueError:
        durr = np.NaN

    return durr


def extract_categories(arr):
    if type(arr["categories"]) == float:
        return np.array([])

    return np.array(arr["categories"].split("|"))


def onehot_ages(arr):

    arr["enfant"] = 0
    arr["ado"] = 0
    arr["adulte"] = 0

    try:
        age_req = arr["age_required"].split("-")
        min_a = int(age_req[0])
        max_a = int(age_req[1])

        if min_a > max_a:
            max_a = 99

        if min_a < 6:
            arr["enfant"] = 1

        if min_a < 16 and max_a > 7:
            arr["ado"] = 1

        if max_a > 17:
            arr["adulte"] = 1

        return arr

    except Exception:
        arr["enfant"] = 1
        arr["ado"] = 1
        arr["adulte"] = 1

        return arr


def onehot_playes(arr):

    arr["solo"] = 0
    arr["multi"] = 0

    try:
        players = arr["nb_players"].split("-")
        min_j = int(players[0])
        max_j = int(players[1])

        if min_j > max_j:
            max_j = 99

        if min_j == 1:
            arr["solo"] = 1

        if max_j > 1:
            arr["multi"] = 1

        return arr

    except Exception:
        arr["multi"] = 1
        arr["solo"] = 1
        return arr
