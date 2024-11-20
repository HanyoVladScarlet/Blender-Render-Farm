from flask import Blueprint
from services.task_services import TaskServices
import json


ts = TaskServices()
print(ts)

client = Blueprint('client', __name__)


@client.route('/get-info')
def get_info():
    # res = json.dumps({'workers': [k for k in td.task_pool.keys()]})
    # res = json.dumps(ts.get_info())
    # print(res)
    res = 'No info available.'
    return res