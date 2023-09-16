import glob
import os
from pathlib import Path
from db_funcs import *
from cohere_analysis import *
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
ALLOWED_EXTENSIONS = set(["7z", "zip"])


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/visualize", methods=["POST"])
def visualize():
    file_type = request.get_json()["fileType"]
    file_name = request.get_json()["fileName"]
    if file_type == "High Level":
        return "html file"
    else:
        return "html file 2"


@app.route("/chat", methods=["POST"])
def chat():
    question = request.get_json()["question"]
    summaries = ...
    chosen_files = find_files(summaries, question)
    response = reply(files, question)
    return jsonify({"response": response})


@app.route("/upload", methods=["POST"])
def upload():
    # Upload 7z file
    target = UPLOAD_FOLDER
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files["test-post.zip"]  # Change name?
    filename = secure_filename(file.filename)
    destination = "/".join([target, filename])
    file.save(destination)
    # Extract 7z file
    Archive(destination).extractall(target)

    # Upload to mongo
    upload_file_mongo(target, filename.split(".")[0])
    print(get_file("test-post", "folder1/sample1.txt"))
    return "Success"


if __name__ == "__main__":
    dbname = get_database()
    app.run(threaded=True, debug=True, host="0.0.0.0", port=3000)
