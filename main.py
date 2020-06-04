from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_compress import Compress
from os import mkdir
from os.path import exists, join
import re
import base64
import requests

from utils import CLASSES, generate_filename, generate_validation_id
from db import init_database, insert_recordings, insert_validations, get_recordings_from_different_user, get_validation, update_validations, \
    VALIDATION_RESULT_CORRECT, VALIDATION_RESULT_INCORRECT, VALIDATION_RESULT_NOT_DONE

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
Compress(app)
app.config['COMPRESS_MIMETYPES'] = ['text/html', 'text/css', 'text/xml',
                                    'application/json', 'application/javascript', 'audio/x-wav']
app.config['COMPRESS_LEVEL'] = 7
app.config['COMPRESS_MIN_SIZE'] = 30

DATASET_DIRECTORY = "Dataset"


@app.before_first_request
def init():
    init_database()
    if (not exists(DATASET_DIRECTORY)):
        mkdir(DATASET_DIRECTORY)


MSSV_REGEX = re.compile("^20\\d{6}$")
NUM_CLASSES = len(CLASSES)


@app.route('/api/speak-submit', methods=['POST'])
def speak_submit():
    try:
        authorId = request.form['authorId']
        recordings = []
        for item in request.files:
            if (item not in CLASSES):
                continue
            class_path = join(DATASET_DIRECTORY, item)
            if (not exists(class_path)):
                mkdir(class_path)
            file = request.files[item]
            filename = generate_filename(authorId, 'wav')
            filepath = join(class_path, filename)
            file.save(filepath)
            recordings.append((filepath, authorId, item))
        insert_recordings(recordings)
        if ('mssv' in request.form and len(recordings) == NUM_CLASSES):
            mssv = request.form['mssv']
            if (MSSV_REGEX.match(mssv)):
                request_data = {
                    'mssv': mssv
                }
                # res = requests.post(
                #     'https://pitec.xfaceid.vn/attendance_api', json=request_data)
                # if (res.status_code != 200):
                #     return ('', 400)
    except:
        return ('', 400)
    return ('', 200)


@app.route('/api/get-validation-requests', methods=['POST'])
def get_validation_requests():
    try:
        userId = request.get_json()['userId']
        recordings = get_recordings_from_different_user(userId)
        result = []
        validations = []
        for i in range(len(recordings)):
            (filename, label) = recordings[i]
            validation_id = generate_validation_id(userId, i)
            result.append({
                'validationId': validation_id,
                'label': label
            })
            validations.append(
                (validation_id, filename, VALIDATION_RESULT_NOT_DONE))
        insert_validations(validations)
        return (jsonify(result), 200)
    except:
        return ('', 400)


@app.route('/api/get-validation-audio', methods=['POST'])
def get_validation_audio():
    try:
        validation_id = request.get_json()['validationId']
        validation = get_validation(validation_id)
        if (validation == None):
            return ('', 400)
        (validation_id, filepath, result) = validation
        if (result != VALIDATION_RESULT_NOT_DONE):
            return ('', 400)
        return send_file(filepath)
    except:
        return ('', 400)


@app.route('/api/validation-submit', methods=['POST'])
def validation_submit():
    try:
        data = request.get_json()
        validations = []
        for item in data:
            validation_id = item['validationId']
            result = item['result']
            if (not isinstance(result, bool)):
                return ('', 400)
            result = VALIDATION_RESULT_CORRECT if result else VALIDATION_RESULT_INCORRECT
            validations.append((result, validation_id))
        update_validations(validations)
    except:
        return ('', 400)
    return ('', 200)
