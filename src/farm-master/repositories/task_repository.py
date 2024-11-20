from queue import Queue
from datetime import datetime as dt
from threading import Lock
from models.render_task import RenderTask
# from models.render_worker import RenderWorker


class TaskDispatcher():
    def __init__(self, max_count=512):
        self.lock = Lock()
        self.task_name = None
        self.status = {}
        # Make this pool a queue.
        # Dequeue only when a task is submitted sucessfully.
        self.task_queue = Queue(maxsize=max_count) 
        self.task_pool = {}

        # This is for test.
        for i in range(300):
            self.task_queue.put(RenderTask().set_token(f'task_{i}'))
        

    def any_available_task(self):
        '''
        True if there are any tasks in task queue.
        '''
        return self.task_queue.qsize() > 0


    def add_one_task(self, data):
        '''
        Input should contain information as following.
        Client username and password.
        Task metadata, including file data.
        Task tag, tasks in the same tag will share the same blender file and python file.
        Blender render settings.
        Blender output settings.
        '''
        new_task = RenderTask()
        with self.lock:
            self.task_queue.put(new_task)


    def get_one_task(self, worker_name):
        # Dispatch a task to caller. 
        if self.task_queue.qsize() == 0:
            return 'No task available!' 
        with self.lock:
            task = self.task_queue.get()
            print()
            print(self.task_pool.keys())

            # Repeat request before last task finishes.
            # Status code -1 means in process.
            if worker_name in self.task_pool.keys():
                pooled_task = self.task_pool[worker_name]
                if pooled_task['status'] == -1:
                    return 'Task already assigned!'
                
            self.task_pool[worker_name] = {
                'task': task,
                'status': -1,
                'last_alive': dt.now().timestamp(),
            }
            res = RenderTask().set_token(task.token)

            return res


    def heartbeat(self, data):
        '''
        + If too long from last report, abort the task and re-enqueue it into task queue.
        + When hearing the heartbeat from a worker for the first time, there shall be a request to collect device information in the response.
        '''
        # if data['code'] == 0:
        #     self.sheep_pool[token].available = True       
        if 'worker_name' not in data.keys() or data['worker_name'] not in self.task_pool:
            print(f'Illegal worker {data["worker_name"]}!')
        if 'status' in data.keys():
            # print(f'Worker {data["worker_name"]} is at {data["status"]}')
            worker_name = data['worker_name']

            if worker_name not in self.workers.keys():
                print(worker_name)
                self.workers[worker_name] = {
                    'ip_addr': data['ip_addr'],
                    'last_alive': dt.now().timestamp()
                }


    def submit_one_task(self, data):
        # Enqueue to task pool for reassignment if failed to validate by metadata.
        with self.lock:
            if 'worker_name' not in data.keys():
                return 'Illegal data!'
            worker_name = data['worker_name']
            print(self.task_pool.keys())
            if not data or 'res' not in data.keys() or data['res'] != 'finished':
                with self.lock:
                    self.task_queue.put(pooled_task)
                print('Task quit with unexpected error!')
            pooled_task = self.task_pool.pop(worker_name)
            print(f'pooled task: {pooled_task}')
            worker_name = data['worker_name']
            return 'Submit successfully.'
