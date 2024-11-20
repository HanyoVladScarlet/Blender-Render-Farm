from flask import Blueprint, render_template, request
import json

from services.task_services import TaskServices
from services.worker_services import WorkerServices
ts = TaskServices()
print(ts)



worker = Blueprint('worker', __name__)


@worker.route('/get-one-task/<worker_name>', methods=['GET'])
def get_one_task(worker_name):
    msg, task = ts.get_one_task(worker_name)
    if task is None:
        return msg

    data = {
        'token': task.token,
        'task_info': 'for test',
        'assets_link': '/download-assets',
        'assets_md5': '',
        'addons_link': '/download-addons',
        'addons_md5': '',
    }
    return data

@worker.route('/heartbeat', methods=['POST'])
def status_report():
    data = json.loads(request.data)
    print(data)
    data['ip_addr'] = request.remote_addr
    ts.heartbeat(data)
    print(f'{request.remote_addr} status: {data}')
    res = {
        'status': 'I hire u.'
    }
    return res 

@worker.route('/submit-one-task', methods=['POST'])
def submit_one_task():
    data = json.loads(request.data) 
    res = ts.submit_one_task(data)
    return res