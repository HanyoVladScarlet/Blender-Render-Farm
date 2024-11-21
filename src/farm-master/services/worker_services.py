from utils.singleton import Singleton
from repositories.worker_repository import WorkerUnion


class WorkerServices():
    def __init__(self):
        self.wu = WorkerUnion()


    def post_heartbeat(self, data):
        '''
        Update the status to union to check for whether it is alive.
        '''
        if 'worker_name' in data and 'status' in data:
            self.wu.update_one_status(data['worker_name'], data['work_status'])
        return
    
    def post_register_worker(self, data):
        '''
        Param data is a dict.
        '''
        return self.wu.add_one_worker(data)
    
    def heartbeat(self, data):
        return self.wu.update_one_status(data)