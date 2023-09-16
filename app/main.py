import glob
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from flask import Flask, flash, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from pyunpack import Archive
from sqlalchemy import asc, func
from werkzeug.utils import secure_filename

load_dotenv()
UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = set(["7z"])


def get_database():
    client = MongoClient(os.environ.get("CONNECTION_STRING"))
    return client["uploads"]


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET"])
def index():
    return "Hello World"


@app.route("/upload", methods=["POST"])
def upload():
    # Upload 7z file
    target = UPLOAD_FOLDER
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files["sample.7z"]  # Change name?
    filename = secure_filename(file.filename)
    destination = "/".join([target, filename])
    file.save(destination)
    # Extract 7z file
    Archive(destination).extractall(target)
    print(target, filename.split(".")[0])
    # Upload to mongo
    upload_file_mongo(target, filename.split(".")[0])
    return "Success"


def upload_file_mongo(target, folder):
    # Get db and create collection
    dbname = get_database()
    collection_name = dbname[folder]
    data = []
    structure = ""
    # Iterate through the files
    path = Path(os.path.dirname(os.path.realpath(__file__))) / target / folder
    for filename in glob.iglob(f"{path}/**", recursive=True):
        if os.path.isfile(filename):
            mongo_filepath = os.path.relpath(filename, path)
            with open(filename, "r") as file:
                file_content = file.read()
                print(file_content)
                file_data = {"filename": mongo_filepath, "data": file_content}
                structure += f"{mongo_filepath}\n"
                data.append(file_data)
    # upload data
    if len(data) > 0:
        delete_all(collection_name)
        data.append({"filename": "structure", "data": structure})
        collection_name.insert_many(data)


def delete_all(collection_name):
    collection_name.delete_many({})


def get_all(collection_name):  # collection_name is the "folder"
    dbname = get_database()
    collection = dbname[collection_name]
    file_details = collection.find()
    print(list(file_details))


def get_file(collection_name, filename):  # collection_name is the "folder"
    dbname = get_database()
    collection = dbname[collection_name]
    file_details = collection.find({"filename": filename})
    print(list(file_details))


if __name__ == "__main__":
    dbname = get_database()
    app.run(threaded=True, debug=True, host="0.0.0.0", port=5000)
