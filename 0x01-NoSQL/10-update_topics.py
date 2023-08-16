#!/usr/bin/env python3
""" updates documents in a collection """


def update_topics(mongo_collection, name, topics):
    """ Updates a School document using kwargs """

    if mongo_collection is None:
        return None
    
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}})
