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

@client.route('/upload/webui', methods=['POST'])
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

@client.route('/upload/client', methods=['POST'])
def add_bpy_task():
    '''
    Post to this api to add a render task with bpy attached.
    '''
    # print(request.files['blend'].filename)
    print(request.data)
    raw_data = json.loads(request.data) 
    if 'upload' not in raw_data: 
        raise Exception('Missing upload data')

    u_config = raw_data['upload']

    if 'username' not in u_config or 'tag' not in u_config or 'with_bpy' not in u_config:
        raise Exception('Illegal upload u_config!')
    user_name = u_config['username']
    tag_name = u_config['tag']

    file = None
    if 'blend' in raw_data:
        file = raw_data['blend']
    if not file or file.filename == 'blend.zip':
        print('No file or wrong formatted file uploaded!')

    # Format see task_repository.add_one_task method.
    data = {
        'username': u_config['username'],
        'tag':  u_config['tag'],
        'with_bpy': u_config['with_bpy'],
        'blender': {}
    }
    # Append blender parameters to data.
    if 'blender' in raw_data:
        data['blender'] = raw_data['blender']

    # Append a task to task queue.
    res = ts.add_one_task(data)
    res = {"code": 0}
    # 
    if file:
        fs.upload_file(user_name, tag_name, file)
    return res