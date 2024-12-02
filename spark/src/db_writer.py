from pymongo import MongoClient
from py2neo import Graph
import json

def write_to_mongodb(data):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['statsbomb']
    collection = db['events']
    collection.insert_many(data)

def write_to_neo4j(data):
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
    for event in data:
        player = event['player']
        event_type = event['event_type']
        query = f"""
        MERGE (p:Player {{name: '{player}'}})
        MERGE (e:Event {{type: '{event_type}'}})
        MERGE (p)-[:PERFORMED]->(e)
        """
        graph.run(query)
