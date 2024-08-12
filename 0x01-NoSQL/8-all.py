#!/usr/bin/env python3
"""
Module for listing all documents in a MongoDB collection
"""


def list_all(mongo_collection):
    """Lists all documents in a collection.
    """
    return list(mongo_collection.find());
