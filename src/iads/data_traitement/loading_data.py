import bson
import csv
import pandas as pd
import os.path


def read_data(filename):
    """
    Function to read data from a BSON file
    """
    bs = open(f'../data/trictrac/{filename}', 'rb').read()

    # List to store decoded data
    dicts = []
    for valid_dict in bson.decode_all(bs):
        dicts.append(valid_dict)

    # Return decoded data
    return dicts


def dump_dicts_to_csv(data, schema, filename):
    """
    Function to write data to a CSV file
    """
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=schema)
        writer.writeheader()
        writer.writerows(data)


def get_schema(data):
    """
    Function to get data schema
    """
    schema = set()

    for d in data:
        schema = schema.union(d.keys())

    return schema


def load_dataframe(filename):
    """
    Function to load data into a dataframe
    """
    # Get base file name
    base_filename = filename.split(".")[0]

    # If csv already exists
    if os.path.exists(f"../data/{base_filename}.csv"):
        return pd.read_csv(f"../data/{base_filename}.csv")

    # Read data from BSON file
    data = read_data(filename)

    # Get data schema
    schema = get_schema(data)

    # Write data to CSV file
    dump_dicts_to_csv(data, schema, f"../data/{base_filename}.csv")

    # Load data into dataframe
    df = pd.read_csv(f"../data/{base_filename}.csv")

    # Check data consistency
    assert df.shape[0] == len(data), "Error loading data"

    return df
