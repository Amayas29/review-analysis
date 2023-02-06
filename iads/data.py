import bson
import csv
import pandas as pd


def read_data(filename):
    """
    Fonction pour lire les données à partir d'un fichier BSON
    """

    bs = open(f'../trictrac_data/{filename}', 'rb').read()

    # Liste pour stocker les données décodées
    dicts = []
    for valid_dict in bson.decode_all(bs):
        dicts.append(valid_dict)

    # Renvoi des données décodées
    return dicts


def dump_dicts_to_csv(data, schema, filename):
    """
    Fonction pour écrire les données dans un fichier CSV
    """

    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=schema)
        writer.writeheader()
        writer.writerows(data)


def get_schema(data):
    """
    Fonction pour obtenir le schéma des données
    """

    schema = set()

    for d in data:
        schema = schema.union(d.keys())

    return schema


def load_dataframe(filename):
    """
    Fonction pour charger les données dans un dataframe
    """

    # Obtention du nom de base du fichier
    base_filename = filename.split(".")[0]

    # Lecture des données à partir du fichier BSON
    data = read_data(filename)

    # Obtention du schéma des données
    schema = get_schema(data)

    # Ecriture des données dans un fichier CSV
    dump_dicts_to_csv(data, schema, f"../data/{base_filename}.csv")

    # Chargement des données dans un dataframe
    df = pd.read_csv(f"../data/{base_filename}.csv")

    # Vérification de la cohérence des données
    assert df.shape[0] == len(data), "Erreur lors du chargement des données"

    return df
