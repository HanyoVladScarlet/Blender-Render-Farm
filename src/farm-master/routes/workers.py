from flask import Blueprint, render_template, request
import json
from hashlib import md5
from zipfile import ZipFile

from services.task_services import TaskServices
from services.worker_services import WorkerServices

ws = WorkerServices()
ts = TaskServices()


worker = Blueprint('worker', __name__)


@worker.route('/get-one-task/<worker_name>', methods=['GET'])
def get_one_task(worker_name):
    res = ts.get_one_task(worker_name)
    code = res['code']
    task = res['task']
    file_path = f'blender_files/{task.username}/{task.tag}/{task.filename}'
    d_link = f'/downloads/{task.username}/{task.tag}'
    with open(file_path, 'rb') as f:
        md5_code = str(md5(f.read()))

        if task:
            data = {
                'code': code,
                'token': task.token,
                'task_info': 'for test',
                'd_link': d_link,
                'd_md5': md5_code,
            }
            return data
    
    return {'code': 1, 'msg': 'No task available.'}


@worker.route('/heartbeat', methods=['POST'])
def status_report():
    data = json.loads(request.data)
    if 'worker_name' in data and 'status' in data:
        ws.heartbeat(data)
    print(f'{request.remote_addr} status: {data}')
    res = {
        'status': 'I hire u.'
    }
    return res 

@worker.route('/submit', methods=['POST'])
def submit_one_task():
    data = json.loads(request.data) 
    file = request.files[file]
    save_path = f'blender_files/{data["username"]}/{data["tag"]}/{data["token"]}'
    if data['with_bpy']:
        save_path += '.zip'
    else:
        save_path += '.png'
    with open(save_path, 'wb') as f:
        f.write(file)
    if data['with_bpy']:
        with ZipFile(save_path, 'r') as f:
            f.extractall()
    print(data)
    res = ts.submit_one_task(data)
    return res
