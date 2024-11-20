from repositories.task_repository import TaskDispatcher
from utils.singleton import Singleton
from datetime import datetime as dt

ILLEGAL_INFO_WARNING = 'Unsupported info sheet, ILLEGAL!'
ILLEGAL_WORKER_WARNING = 'Unregistered worker, ILLEGAL!'


@Singleton
class WorkerUnion():
    '''
    Use this repository for worker register.
    '''
    def __init__(self):
        self.td = TaskDispatcher()
        '''
        Worker map is used for register worker with their device info, task history, and current status.
        {
            "status": 0, 1, 2,
            "last_alive": <timestamp>
            "device_info": { ... },
            "task_history": { ... }
        }
        '''
        self.worker_map = {}

    def add_one_worker(self, data):
        '''
        + Add a worker to worker map, override if existed.
        + The param worker_data should have a key worker_name with value as worker_data core.
        + In principle, there is only one worker on one machine.
        + Formatted as following.
        {
            "worker_name": "{username}@{hostname}",
            "worker_data": 
            {
                "status": 0, 1, 2,
                "last_alive": <timestamp>
                "device_info": { ... },
                "task_history": { ... }
            }
        }
        '''
        if 'worker_name' not in data.keys():
            print(ILLEGAL_INFO_WARNING)
            return    
        worker_name = data['worker_name']
        worker_item = {
            'status': data['worker_status'],
            'last_alive': dt.now().timestamp(),
            'device_info': data['device_info'],
            'task_history': {}
        }
        self.worker_map[worker_name] = worker_item
        return


    def get_one_worker(self, worker_name):
        '''
        Get one worker by name.
        '''
        if worker_name in self.worker_map.keys():
            return self.worker_map[worker_name]
        return 
    
    def get_one_task(self, worker_name):
        if not self.td.any_available_task():
            return 'No task available.'
        res = self.td.get_one_task(worker_name)
        return res

    def update_one_status(self, worker_name, status):
        if worker_name not in self.worker_map.keys():
            return ILLEGAL_WORKER_WARNING
        self.worker_map[worker_name]['status'] = status
        self.worker_map[worker_name]['last_alive'] = dt.now().timestamp()
        return