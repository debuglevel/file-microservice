#!/bin/usr/python3
from flask import Flask
from flask import send_file
from flask import request
from flask import send_from_directory, jsonify, make_response
import sys
import tempfile
import uuid
import os
import shutil
import base64
import uuid
import json
from tinydb import TinyDB, Query

app = Flask(__name__)

DATA_DIRECTORY = '/data'
print('Starting up File microservice...', file=sys.stderr)

db = TinyDB(f'{DATA_DIRECTORY}/db.json')

@app.route("/health")
def health():
    print('Received GET request on /health', file=sys.stderr)
    return jsonify(
        {
         "status": "up",
         "files_count": len(db),
        }
    )

@app.route('/files/', methods=['POST'])
def upload_file():
    print(f"POST /files/")
    print(f"Content-Type: {request.content_type}")
    print(f"Content-Length: {request.content_length}")
    data = request.get_data()
    print(f"Length of data: {len(data)}")

    myUuid = uuid.uuid4()
    print(f"UUID: {myUuid}")

    metadata = { 
        "uuid": str(myUuid),
        "content_type": request.content_type,
        "content_length": request.content_length,
        "size": len(data),
     }

    print(f"Inserting metadata for {myUuid} into database...")
    db.insert(metadata)

    with open(f"{DATA_DIRECTORY}/{myUuid}", "wb") as myfile:
        print(f"Writing data for {myUuid} to file {myfile.name}...")
        myfile.write(data)
        print(f"Wrote data for {myUuid} to file {myfile.name}")

    print(f"Returning metadata for {myUuid} to client...")


    response = make_response(jsonify(metadata), 201)
    response.headers["Content-Type"] = "application/json"
    response.headers["Location"] = f"/files/{myUuid}"
    return response

@app.route('/files/<myUuid>', methods=['GET'])
def download_file(myUuid: str):
    print(f"GET /files/{myUuid}")
    print(f"UUID: {myUuid}")

    print(f"Getting metadata for {myUuid} from database...")
    Metadata = Query()
    metadata = db.get(Metadata.uuid == myUuid)
    print(f"Got metadata for {myUuid} from database: {metadata}")
    content_type = metadata["content_type"]

    with open(f"{DATA_DIRECTORY}/{myUuid}") as file:
        print(f"Sending data for {myUuid} to client...")
        return send_file(file.name, attachment_filename=f"{myUuid}", mimetype=f"{content_type}")

@app.route('/files/<myUuid>', methods=['DELETE'])
def delete_file(myUuid: str):
    print(f"DELETE /files/{myUuid}")
    print(f"UUID: {myUuid}")

    print(f"Getting metadata for {myUuid} from database...")
    Metadata = Query()
    metadata = db.get(Metadata.uuid == myUuid)
    print(f"Got metadata for {myUuid} from database: {metadata}")

    print(f"Removing metadata for {myUuid} from database...")
    db.remove(Metadata.uuid == myUuid)
    print(f"Removed metadata for {myUuid} from database")

    print(f"Deleting file for {myUuid}...")
    os.remove(f"{DATA_DIRECTORY}/{myUuid}")
    print(f"Deleted file for {myUuid}")

    return '', 204
