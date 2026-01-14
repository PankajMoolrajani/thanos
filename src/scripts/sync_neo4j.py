#!/usr/bin/env python3
"""
Script to sync YAML data to Neo4j database.
Creates/updates nodes and relationships without duplicates using MERGE operations.
"""

import argparse
import os
import sys
from pathlib import Path

import yaml
from neo4j import GraphDatabase


# Neo4j connection configuration - uses environment variables for local/cloud flexibility
# For local development (Docker): NEO4J_URI=bolt://neo4j:7687
# For cloud: Set the appropriate cloud URI
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "thanos_password")

def get_args(): 
    parser = argparse.ArgumentParser(description='Sync YAML data to Neo4j database.')
    parser.add_argument('--yaml-file', type=str, required=True, help='Path to the YAML file to sync.')
    return parser.parse_args()


def load_yaml_data(yaml_file):
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    return data


def get_nodes(data):
    nodes = []
    for item in data['nodes']:
        nodes.append(item)
    return nodes

def get_relationships(data):
    relationships = []
    for item in data['relationships']:
        relationships.append(item)
    return relationships


def get_neo4j_client():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def check_if_node_exists(node):
    print (f"CHECKING IF NODE {node['id']} EXISTS")
    neo4j_client = get_neo4j_client()
    query = f"MATCH (n) WHERE n.id = '{node['id']}' RETURN n"
    print (query)
    result = neo4j_client.execute_query(query)
    
    if result.records:
        print(f"Node {node['id']} exists")
        return True
    else:
        print(f"Node {node['id']} does not exist")
        return False

def create_node(node):
    neo4j_client = get_neo4j_client()
    print (f"CREATING NODE {node['id']}")
    # Build the labels string for the query
    labels_str = ":".join(node["labels"])
    query = f"CREATE (n:{labels_str}) SET n = $properties"
    params = {
        "properties": node["properties"]
    }
    session = neo4j_client.session()
    result = session.run(query, params)
    return result.single() is not None

def update_node(node):
    neo4j_client = get_neo4j_client()
    print (f"UPDATING NODE {node['id']}")
    # Build the labels string for the query
    labels_str = ":".join(node["labels"])
    
    query = f"""
        MATCH (n)
        WHERE n.id = $id
        SET n:{labels_str}
        SET n = $properties
    """
    params = {
        "id": node["id"],
        "properties": node["properties"]   
    }
    session = neo4j_client.session()
    result = session.run(query, params)
    return result.single() is not None

def create_or_update_nodes(nodes):
    print (f"CREATING OR UPDATING NODES")
    for node in nodes:
        # check if node exists
        if check_if_node_exists(node):
            print(f"Node {node['id']} already exists")
            update_node(node)
            print(f"Node {node['id']} updated")
        else:
            print(f"Node {node['id']} does not exist")
            create_node(node)
            print(f"Node {node['id']} created")

def check_if_relationship_exists(relationship):
    print (f"CHECKING IF RELATIONSHIP {relationship['source_node_id']} -> {relationship['target_node_id']} ({relationship['relation_type']}) EXISTS")
    neo4j_client = get_neo4j_client()
    query = f"""
        MATCH (source {{id: '{relationship['source_node_id']}'}})
        MATCH (target {{id: '{relationship['target_node_id']}'}})
        MATCH (source)-[rel:{relationship['relation_type']}]->(target)
        RETURN rel
    """
    print (f"Query: {query}")
    result = neo4j_client.execute_query(query)
    return len(result.records) > 0

def create_relationship(relationship):
    print (f"CREATING RELATIONSHIP {relationship['source_node_id']} -> {relationship['target_node_id']} ({relationship['relation_type']})")
    neo4j_client = get_neo4j_client()
    # Build the query to match source and target nodes, then merge the relationship
    query = f"""
        MATCH (source {{id: '{relationship['source_node_id']}'}})
        MATCH (target {{id: '{relationship['target_node_id']}'}})
        MERGE (source)-[rel:{relationship['relation_type']}]->(target)
    """

    print(f"Query: {query}")
    session = neo4j_client.session()
    result = session.run(query)
    return result.single() is not None

def update_relationship(relationship):
    print (f"UPDATING RELATIONSHIP {relationship['source_node_id']} -> {relationship['target_node_id']} ({relationship['relation_type']})")
    neo4j_client = get_neo4j_client()
    # Get the relationship type from labels (e.g., HAS_CONTROL_CONDITION, REQUIRES_CONTROL)
    
    query = f"""
        MATCH (source {{id: '{relationship['source_node_id']}'}})
        MATCH (target {{id: '{relationship['target_node_id']}'}})
        MERGE (source)-[rel:{relationship['relation_type']}]->(target)
    """
    print(f"Query: {query}")
    session = neo4j_client.session()
    result = session.run(query)
    return result.single() is not None

def create_or_update_relationships(relationships):
    print (f"CREATING OR UPDATING RELATIONSHIPS")
    for relationship in relationships:
        print (relationship)
        # check if relationship exists
        if check_if_relationship_exists(relationship):
            print(f"Relationship {relationship['source_node_id']} -> {relationship['target_node_id']} ({relationship['relation_type']}) already exists")
            update_relationship(relationship)
            print(f"Relationship {relationship['source_node_id']} -> {relationship['target_node_id']} ({relationship['relation_type']}) updated")
        else:
            print(f"Relationship {relationship['source_node_id']} -> {relationship['target_node_id']} ({relationship['relation_type']}) does not exist")
            create_relationship(relationship)
            print(f"Relationship {relationship['source_node_id']} -> {relationship['target_node_id']} ({relationship['relation_type']}) created")

def main(args):
    yaml_data = load_yaml_data(args.yaml_file)
    nodes = get_nodes(yaml_data)
    relationships = get_relationships(yaml_data)
    # create_or_update_nodes(nodes)
    create_or_update_relationships(relationships)
    print (f"DONE")
if __name__ == '__main__':
    args = get_args()
    main(args)
