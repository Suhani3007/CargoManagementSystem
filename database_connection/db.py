import os
import  psycopg2
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

DB_TYPE=os.getenv("DB_TYPE")

def get_postgres():
    conn=psycopg2.connect(
            dbname=os.getenv("DBNAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
    )
    return conn


def get_mongo():
    mono_url=os.getenv("MONGO_URL")
    db_name=os.getenv("MONGO_DB")
    client=MongoClient(mono_url)
    return client[db_name]


def get_db():
    if DB_TYPE=="postgres":
        return get_postgres()
    elif DB_TYPE=="mongo":
        return get_mongo()
    else:
        return{
            "message":"unsupported type"
        }
