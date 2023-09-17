import glob
import os
from build_graph import build_dependency_graph
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
ALLOWED_EXTENSIONS = set(["7z", 'zip'])





app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/visualize", methods=["POST"])
def visualize():
    file_type = request.get_json()['fileType']
    file_name = request.get_json()['fileName']
    all_data = get_all('src')
    if file_type == 'High Level':
        current_data = {data['filename']: (data['data'], data['summary']) for data in all_data}
        build_dependency_graph()
    else:
        for row in all_data:
            if row['filename'] == file_name:
                data = {file_name: (row['data'], row['summary'])}
        build_dependency_graph(data)


@app.route("/chat", methods=["POST"])
def chat():
    question = request.get_json()['question']
    all_data = get_all('src')

    summaries = {data['summary']: data['filename'] for data in all_data}
    chosen_files = find_files(summaries, question)
    response = reply(files, question)
    return jsonify({
        'response': response
    })



@app.route("/upload", methods=["POST"])
def upload():

    # Upload 7z file
    target = UPLOAD_FOLDER
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files["src.zip"]  # Change name?
    filename = secure_filename(file.filename)
    destination = "/".join([target, filename])
    file.save(destination)
    # Extract 7z file
    Archive(destination).extractall(target)

    # Upload to mongo
    dict_repo = {}
    upload_file_mongo(target, filename.split(".")[0])
    all_info = get_all('src')
    
    folders = {}
    for file in all_info:
        file_name = file['filename']
        splitted = file_name.split('/')
        folder = splitted[0]
        if folder not in folders:
            folders[folder] = {file_name: file['data']}
        else:
            folders[folder][file_name] = file['data']
        dict_repo[file_name] = summarize_code({file_name: file['data']})
    for folder in folders:
        dict_repo[folder] = summarize_code(folders[folder])

    for file in dict_repo:
        add_file_summary('src', file, dict_repo[file])
        
    return "Success"







if __name__ == "__main__":
    dbname = get_database()
    app.run(threaded=True, debug=True, host="0.0.0.0", port=3000)

