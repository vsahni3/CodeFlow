import glob
import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
from pyunpack import Archive


def get_database():
    client = MongoClient(os.environ.get("CONNECTION_STRING"))
    return client["uploads"]


def upload_file_mongo(target, folder):
    # Get db and create collection
    dbname = get_database()
    collection_name = dbname[folder]
    data = []
    # Iterate through the files
    path = Path(os.path.dirname(os.path.realpath(__file__))) / target / folder
    for filename in glob.iglob(f"{path}/**", recursive=True):
        if os.path.isfile(filename):
            mongo_filepath = os.path.relpath(filename, path)
            with open(filename, "r") as file:
                file_content = file.read()
                file_data = {"filename": mongo_filepath, "data": file_content}
                data.append(file_data)
    # upload data
    if len(data) > 0:
        delete_all(collection_name)
        collection_name.insert_many(data)


def get_all(collection_name):  # collection_name is the "folder"
    dbname = get_database()
    collection = dbname[collection_name]
    file_details = collection.find()
    return list(file_details)


def get_file(collection_name, filename):  # collection_name is the "folder"
    
    data = get_all('src')
    for row in data:
        if filename == row['filename']:
            return row



def delete_all(collection_name):
    collection_name.delete_many({})


def add_file_summary(collection_name, filename, summary):
    dbname = get_database()
    collection = dbname[collection_name]
    query = {"filename": filename}
    collection.update_many(query, {"$set": {"summary": summary}})


def add_folder_sumary(collection_name, foldername, summary):
    dbname = get_database()
    collection_name = dbname[collection_name]
    data = {"filename": foldername, "data": "", "summary": summary}
    collection_name.insert_one(data)
