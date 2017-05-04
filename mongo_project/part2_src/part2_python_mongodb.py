# pylint: disable=invalid-name
"""
    python_mongodb.py: Implement simple operations on
        mongo database.
"""

import pprint
import pymongo
import pandas as pd
import numpy as np

__author__ = "Stratos Gounidellis, Lamprini Koutsokera"
__copyright__ = "Copyright 2017, BDSMasters"


def connect_to_mongo(db_name, collection_name):
    """Connect to mongo database and collection.
    :param db_name: The name of the mongo database.
    :param collection_name: The name of the mongo collection.
    :return: A coonection to a collection and a MongoClient
        object.
    """
    try:
        client = pymongo.MongoClient()
        db = client[db_name]
        collection = db[collection_name]
    except pymongo.errors.ConnectionFailure:
        print "Unable to connect to mongo!"
        quit()
    return collection, client


def insert_one(db_name, collection_name, record):
    """Connect to mongo database and collection and insert
        a record.
    :param db_name: The name of the mongo database.
    :param collection_name: The name of the mongo collection.
    :param record: The records to be inserted to the mongo
        collection.
    """
    collection = connect_to_mongo(db_name, collection_name)
    try:
        collection[0].delete_many({})
    except pymongo.errors.ServerSelectionTimeoutError:
        print "Unable to connect to mongo!"
        quit()
    print '\nInserting Christiano to the collection.\n'
    collection[0].insert_one(record)
    collection[1].close()


def insert_many(db_name, collection_name, records_list):
    """Connect to mongo database and collection and insert multiple
        records.
    :param db_name: The name of the mongo database.
    :param collection_name: The name of the mongo collection.
    :param records_list: The records to be inserted to the
        mongo collection.
    """
    print 'Inserting Maria and Dimitris to the collection.\n'
    collection = connect_to_mongo(db_name, collection_name)
    collection[0].insert_many(records_list)
    collection[1].close()


def print_records(db_name, collection_name):
    """Connect to mongo database and collection and print its
        content.
    :param db_name: The name of the mongo database.
    :param collection_name: The name of the mongo collection.
    """
    print "Printing collection's content.\n"
    collection = connect_to_mongo(db_name, collection_name)
    for record in collection[0].find():
        pprint.pprint(record)
    collection[1].close()


def update_collection(db_name, collection_name):
    """Connect to mongo database and collection and update its
        documents.
    :param db_name: The name of the mongo database.
    :param collection_name: The name of the mongo collection.
    """
    print "\nUpdating Christiano's age field."
    collection = connect_to_mongo(db_name, collection_name)
    collection[0].update_one({
        'name': "Christiano"
    }, {
        '$set': {
            'age': 26
        }
    }, upsert=True)

    print "Updating Maria's name."
    collection[0].update_one({
        'name': "Maria"
    }, {
        '$set': {
            'name': "Ioanna"
        }
    }, upsert=True)
    print "Deleting Dimitris."
    collection[0].delete_one({"name": "Dimitris"})
    collection[1].close()


def print_records_field(db_name, collection_name, field):
    """Connect to mongo database and collection and print
        specific field.
    :param db_name: The name of the mongo database.
    :param collection_name: The name of the mongo collection.
    :param field: The name of the field to be printed.
    """
    print "\nPrinting info about " + str(field) + ".\n"
    collection = connect_to_mongo(db_name, collection_name)
    check_exists = False
    for record in collection[0].find():
        if field in record.keys():
            pprint.pprint(record[field])
            check_exists = True
    if not check_exists:
        print "No records with field '" + str(field) + "' were found!"
    collection[1].close()


def mongo_to_df(db_name, collection_name):
    """Connect to mongo database and collection and convert the collection
        to a dataframe.
    :param db_name: The name of the mongo database.
    :param collection_name: The name of the mongo collection.
    :return: A dataframe containing the content of the collection.
    """
    print "\nConverting collection to dataframe.\n"
    collection = connect_to_mongo(db_name, collection_name)
    fields = []
    for record in collection[0].find():
        keys = record.keys()
        for key in keys:
            if key not in fields:
                fields.append(key)

    results_array = np.zeros(len(fields))
    for record in collection[0].find():
        temp_list = []
        for field in fields:
            if field in record.keys():
                temp_list.append(record[field])
            else:
                temp_list.append(None)
        temp_results = np.array(temp_list)
        results_array = np.vstack((temp_results, results_array))
    results_array = results_array[:-1, :]
    df_results = pd.DataFrame(data=results_array, columns=fields)
    collection[1].close()
    return df_results


def df_to_mongo(df, db_name, collection_name):
    """Connect to mongo database and collection and import data
        from a dataframe.
    :param df: The dataframe to import to the mongo collection.
    :param db_name: The name of the mongo database.
    :param collection_name: The name of the mongo collection.
    """
    print "\nImporting dataframe to collection."

    collection = connect_to_mongo(db_name, collection_name)
    for _, row in df.iterrows():
        row_dict = row.to_dict()
        for key in row_dict.keys():
            if row_dict.get(key) is None:
                row_dict.pop(key, None)
            else:
                try:
                    row_dict[key] = int(row_dict.get(key))
                except ValueError:
                    pass
        collection[0].insert_one(row_dict)
    collection[1].close()


if __name__ == "__main__":
    db_name = "project"
    collection_name = "pymongo_project"
    christiano = {"language": "Portuguese", "name": "Christiano"}
    insert_one(db_name, collection_name, christiano)

    maria = {"name": "Maria", "age": 34, "language": "English"}
    dimitris = {"name": "Dimitris", "language": "Greek"}
    records_list = [maria, dimitris]
    insert_many(db_name, collection_name, records_list)

    print_records(db_name, collection_name)

    update_collection(db_name, collection_name)

    print_records_field(db_name, collection_name, "age")

    df_mongo = mongo_to_df(db_name, collection_name)
    print df_mongo

    records_array = np.zeros(3)
    giannis = ["Giannis", None, "German"]
    nikos = ["Nikos", 23, "Polish"]
    clio = ["Clio", 19, "Greek"]
    eleni = ["Eleni", 29, None]
    records = [giannis, nikos, clio, eleni]

    for record in records:
        records_array = np.vstack((record, records_array))
    records_array = records_array[:-1, :]
    df_records = pd.DataFrame(data=records_array,
                              columns=("name", "age", "language"))
    df_to_mongo(df_records, db_name, collection_name)

    df_mongo = mongo_to_df(db_name, collection_name)
    print df_mongo
