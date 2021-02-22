import logging

from pymongo import MongoClient

from ..configs import (
    MONGO_TIMEOUT,
    MONGO_URL
)

class Database:
    client: MongoClient = None

db = Database()

def open_db_connection():
    logging.info('Establishing database connection')
    try:
        db.client = MongoClient(
            MONGO_URL,
            serverSelectionTimeoutMS=MONGO_TIMEOUT
        )
        
        db.client.server_info()
        logging.info('Connected to database successfully')
    except:
        logging.error('Conecting to database failed')

def close_db_connection():
    logging.info('Closing database connection')
    try:
        db.client.close()
        logging.info('Database diconnected successfully')
    except:
        logging.error('Database diconnected failed')

def get_client() -> MongoClient:
    return db.client