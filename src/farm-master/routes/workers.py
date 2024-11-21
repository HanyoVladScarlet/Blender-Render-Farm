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
    if code == 1:
        return {'code': 1, 'msg': 'No task available.'}
    task = res['task']
    file_path = f'blender_files/{task.username}/{task.tag}/blend.zip'
    d_link = f'/downloads/{task.username}/{task.tag}'
    with_bpy = task.with_bpy
    with open(file_path, 'rb') as f:
        md5_code = str(md5(f.read()))

        if task:
            data = {
                'code': code,
                'token': task.token,
                'tag': task.tag,
                'task_info': 'for test',
                'd_link': d_link,
                'd_md5': md5_code,
                'with_bpy': with_bpy
            }
            return data 
        

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
    print(request.files.keys())
    # print(request.json)
    print(request.files['data'])
    data = json.load(request.files['data']) 
    print('cool and good!')
    print(data)
    print('warm and bad!')
    print(request.files.keys())
    file = request.files['file']
    save_path = f'blender_files/{data["username"]}/{data["tag"]}/{data["token"]}'
    if data['with_bpy']:
        save_path += '.zip'
    else:
        save_path += '.png'
    file.save(save_path)
    if data['with_bpy']:
        with ZipFile(save_path, 'r') as f:
            f.extractall()
    print(data)
    res = ts.submit_one_task(data)
    return res
