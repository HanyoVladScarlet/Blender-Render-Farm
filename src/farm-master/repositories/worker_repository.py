from utils.singleton import Singleton
from datetime import datetime as dt
from time import time as t_time
from utils.ticker import Ticker
from models.render_worker import BlenderWorker

ILLEGAL_INFO_WARNING = 'Unsupported info sheet, ILLEGAL!'
ILLEGAL_WORKER_WARNING = 'Unregistered worker, ILLEGAL!'


@Singleton
class WorkerUnion():
    '''
    Use this repository for worker register.
    '''
    def __init__(self):
        '''
        Worker map is used for register worker with their device info, task history, and current status.
        {
            "status": 0, 1, 2,
            "last_alive": <timestamp>
            "device_info": { ... },
            "task_history": { ... }
        }
        '''
        self.worker_list = []
        self.timeout = 10
        Ticker().register(self)


    def tick(self):
        for worker_name in self.worker_list:
            if t_time() - self.worker_list[worker_name]['last_alive'] > self.timeout:
                self.worker_list[worker_name]['status'] = 2
        return

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
        if 'worker_name' not in data:
            print(ILLEGAL_INFO_WARNING)
            return    
        worker = BlenderWorker()
        worker.name = data['worker_name']
        worker.is_busy = False,
        worker.last_alive = dt.now().timestamp()
        worker.device_info = data['qpu-status']
        self.worker_list.append(worker)
        return


    def get_one_worker(self, worker_name):
        '''
        Get one worker by name.
        '''
        if worker_name in [w.name for w in self.worker_list]:
            return self.worker_list[worker_name]
        return 
    
    def is_worker_alive(self, worker_name):
        '''
        Find out is a worker alive.
        '''
        return worker_name not in self.worker_list or self.worker_list[worker_name]['status'] < 2
    
    def get_one_task(self, worker_name):
        if not self.td.any_available_task():
            return 'No task available.'
        res = self.td.get_one_task(worker_name)
        return res

    def update_one_status(self, data):
        if 'worker_name' not in data:
            return {'msg': 'Illegal data'}
        worker_name = data['worker_name']
        for worker in self.worker_list:
            if worker_name == worker.name:
                worker.is_busy = data['status'] == 1
                worker.last_alive = dt.now().timestamp()
                worker.device_info = data['gpu-status']
                return {'msg': 'I hire u.'}
    
    def get_worker_status(self):
        return [{

        }]