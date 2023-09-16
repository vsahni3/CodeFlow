import json
import logging
import os
from argparse import ArgumentParser

import pandas as pd
from dotenv import load_dotenv
from flask import Flask, flash, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, func
from werkzeug.utils import secure_filename

load_dotenv()
# DATABASE_URI = os.environ.get("DATABASE_URI")
UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = set(["py", "zip", "txt"])

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
# app.config["SQLALCHEMY_ECHO"] = False
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)
# app.app_context().push()


@app.route("/", methods=["GET"])
def index():
    return "Hello World"


@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(UPLOAD_FOLDER, "sample_upload_folder")
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files["sample.txt"]
    filename = secure_filename(file.filename)
    destination = "/".join([target, filename])
    file.save(destination)
    return "Success"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
