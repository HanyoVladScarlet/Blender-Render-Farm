from queue import Queue
from datetime import datetime as dt
from threading import Lock
from models.render_task import RenderTask
from uuid import uuid4 as uuid
from repositories.worker_repository import WorkerUnion
from utils.ticker import Ticker
from utils.singleton import Singleton
# from models.render_worker import RenderWorker


@Singleton
class TaskDispatcher():
    def __init__(self, max_count=512):
        self.lock = Lock()
        self.task_name = None
        self.status = {}
        self.wu = WorkerUnion()

        # Make this pool a queue.
        # Dequeue only when a task is submitted sucessfully.
        self.task_queue = Queue(maxsize=max_count) 
        self.task_pool = {}

        Ticker().register(self)
        # This is for test.
        for i in range(300):
            new_task = RenderTask()
            new_task.token = str(uuid())
            new_task.username = 'anonymous'
            new_task.tag = 'demo-tag'
            new_task.timestamp = dt.now().timestamp()
            new_task.filename = 'for_test.blend'
            self.task_queue.put(new_task)
        

    def any_available_task(self):
        '''
        True if there are any tasks in task queue.
        '''
        return self.task_queue.qsize() > 0


    def tick(self):
        to_be_poped = []
        with self.lock:
            for worker_name in self.task_pool:
                if not self.wu.is_worker_alive(worker_name):
                    to_be_poped.append(worker_name)
            for w in to_be_poped:
                self.requeue(worker_name)
                

    def requeue(self, worker_name):
        if worker_name in self.task_pool:
            task = self.task_pool.pop(worker_name)
            task_item = task['task']
            self.task_queue.put(task_item)
            print(f'Task {task_item.token} has returned to task queue.')


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
        new_task.token = str(uuid())
        new_task.username = data['username']
        new_task.tag = data['tag']
        new_task.timestamp = dt.now().timestamp()
        new_task.filename = data['filename']
        
        with self.lock:
            self.task_queue.put(new_task)


    def get_one_task(self, worker_name):
        print(self.task_pool)
        # Dispatch a task to caller. 
        if self.task_queue.qsize() == 0:
            return  {'code': 1, 'task': None}
        
        # Repeat request before last task finishes.
        # Status code -1 means in process.
        if worker_name in self.task_pool:
            return {'code': 2, 'task': self.task_pool[worker_name]['task']}
            
        with self.lock:
            task = self.task_queue.get()
            self.task_pool[worker_name] = {
                'task': task,
                'status': -1,
                'last_alive': dt.now().timestamp(),
            }
            print(self.task_pool)
            return {'code': 0, 'task': task}


    def submit_one_task(self, data):
        # Enqueue to task pool for reassignment if failed to validate by metadata.
        # TODO: How to validate whether task is completed is to be decided.
        with self.lock:
            if 'worker_name' not in data:
                return 'Illegal data!'
            worker_name = data['worker_name']
            print(self.task_pool)
            if not data or 'code' not in data or data['code'] != 0:
                self.requeue(worker_name)
                print('Task quit with unexpected error!')
            pooled_task = self.task_pool.pop(worker_name)
            print(f'pooled task: {pooled_task}')
            worker_name = data['worker_name']
            return 'Submit successfully.'