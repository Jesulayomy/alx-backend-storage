#!/usr/bin/env python3
""" Lists all documents in a collection """


def list_all(mongo_collection):
    """ This function lists all the docs in collection"""

    if mongo_collection is None:
        return []
    
    return mongo_collection.find()
