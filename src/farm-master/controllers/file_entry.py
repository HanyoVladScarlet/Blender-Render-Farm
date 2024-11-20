from flask import Blueprint, send_file, abort, request
from services.file_services import FileServices
from werkzeug.utils import secure_filename

import json


fs = FileServices()

file_entry = Blueprint('file_entry', __name__)


@file_entry.route('/downloads/assets/<file_name>', methods=['GET'])
def get_assets(file_name):
    try:
        print(file_name)
        f_path = fs.get_file()
        return send_file(f_path)
    except Exception as e:
        # abort('404')
        print(e)
        return 'Asset not found!'

@file_entry.route('/downloads/addons/<file_name>', methods=['GET'])
def get_addons(file_name):
    try:
        f_path = fs.get_file(file_name)
        return send_file(f_path)
    except:
        # abort('404')
        return 'Addon not found!'
    

# By Microsoft Copilot.
@file_entry.route('/api/upload', methods=['POST'])
def upload_file():
    # print(request.data)
    # data = json.loads(request.data)
    print(request.files)
    key = [k for k in request.files.keys()][0]
    print(key)
    file = request.files[key]
    print(file.filename)
    if file.filename == '':
        return 'No file uploaded!'
    if file:
        filename = secure_filename(file.filename)
        fs.upload_file('anonymous', 'demo_tag', file)
    # return
    return ''