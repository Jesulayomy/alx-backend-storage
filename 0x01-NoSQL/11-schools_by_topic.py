#!/usr/bin/env python3
"""
    A Python function that returns the list of school
    having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """ find db by a specific topic """

    if mongo_collection is None:
        return None
    return mongo_collection.find({"topics": topic})
