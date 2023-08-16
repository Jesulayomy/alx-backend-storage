#!/usr/bin/env python3
""" insert documents in a collection """


def insert_school(mongo_collection, **kwargs):
    """ Inserts a School document using kwargs """

    if mongo_collection is None:
        return None
    
    return mongo_collection.insert_one(kwargs).inserted_id
