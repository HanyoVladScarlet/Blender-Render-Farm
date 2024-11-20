from utils.singleton import Singleton
from repositories.worker_repository import WorkerUnion


class WorkerServices():
    def __init__(self):
        self.wu = WorkerUnion()


    def post_heartbeat(self, data):
        '''
        Update the status to union to check for whether it is alive.
        '''
        if 'worker_name' in data.keys() and 'worker_status' in data.keys():
            self.wu.update_one_status(data['worker_name'], data['work_status'])
        return
    def post_register_worker(self, data):
        '''
        Param data is a dict.
        '''
        return self.wu.add_one_worker(data)

    def get_task(self, worker_name):
        return self.wu.get_one_task(worker_name)