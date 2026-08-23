# MongoDB connection and operations
# Manages all database interactions

from pymongo import MongoClient

class MongoDatabase:
    """MongoDB database handler."""
    
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client.senrivia
