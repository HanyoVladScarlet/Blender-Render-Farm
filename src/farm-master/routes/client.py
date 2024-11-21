from flask import Blueprint, request
from services.task_services import TaskServices
from services.file_services import FileServices
import json


ts = TaskServices()
fs = FileServices()
client = Blueprint('client', __name__)


@client.route('/get-info')
def get_info():
    res = 'No info available.'
    res = json.dumps(ts.get_task_queue())
    return res


# By Microsoft Copilot.
@client.route('/upload/with-bpy', methods=['POST'])
def upload_bpy_file():
    # print(request.data)
    # print(request.form)
    # data = json.loads(request.data)
    # print(request.files)
    form = request.form
    user_name = 'anonymous'
    tag_name = 'demo-tag'
    file = None
    if 'username' in form:
        user_name = form['username']
    if 'tag' in form:
        tag_name = form['tag']
    if 'blend' in request.files:
        file = request.files['blend']
    if file.filename == '':
        return 'No file uploaded!'
    if file:
        '''
        Format see task_repository.add_one_task method.
        '''
        res = ts.add_one_task({
            'username': user_name,
            'tag': tag_name,
            'filename': file.filename,
            'with_bpy': True,
        })
        fs.upload_file(user_name, tag_name, file)
    # return
    return ''

@client.route('/upload/single', methods=['POST'])
def add_single_task():
    '''
    Post to this api to render single image.
    '''
    form = request.form
    user_name = 'anonymous'
    tag_name = 'demo-tag'
    file = None
    if 'username' in form:
        user_name = form['username']
    if 'tag' in form:
        tag_name = form['tag']
    if 'blend' in request.files:
        file = request.files['blend']
    if file.filename == '':
        return 'No file uploaded!'
    if file:
        '''
        Format see task_repository.add_one_task method.
        '''
        res = ts.add_one_task({
            'username': user_name,
            'tag': tag_name,
            'filename': file.filename,
            'with_bpy': False,
        })
        fs.upload_file(user_name, tag_name, file)
    # return
    return res

@client.route('/upload/bpy', methods=['POST'])
def add_bpy_task():
    '''
    Post to this api to add a render task with bpy attached.
    '''
    form = request.form
    user_name = 'anonymous'
    tag_name = 'demo-tag'
    file = None
    if 'username' in form:
        user_name = form['username']
    if 'tag' in form:
        tag_name = form['tag']
    if 'blend' in request.files:
        file = request.files['blend']
    if file.filename == '':
        return 'No file uploaded!'
    if file:
        '''
        Format see task_repository.add_one_task method.
        '''
        res = ts.add_one_task({
            'username': user_name,
            'tag': tag_name,
            'filename': file.filename,
            'with_bpy': True,
        })
        fs.upload_file(user_name, tag_name, file)
    # return
    return res