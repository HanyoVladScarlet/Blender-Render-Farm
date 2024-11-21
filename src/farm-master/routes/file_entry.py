from flask import Blueprint, send_file, abort, request
from services.file_services import FileServices
from werkzeug.utils import secure_filename

import json


fs = FileServices()

file_entry = Blueprint('file_entry', __name__)


@file_entry.route('/downloads/assets/<user_name>/<tag_name>', methods=['GET'])
def get_assets(user_name, tag_name):
    '''
    Default name of the target zip file is "blend.zip"
    '''
    try:
        f_path = fs.get_file(user_name, tag_name)
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
    

@file_entry.route('/downloads/<user_name>/<tag_name>', methods=['GET'])
def get_files(user_name, tag_name):
    try:
        f_path = fs.get_file(user_name, tag_name)
        return send_file(f_path)
    except Exception as e:
        # abort('404')
        print(e)
        return 'Asset not found!'