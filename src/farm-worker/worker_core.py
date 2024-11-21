import os
from time import sleep
from threading import Lock
from platform import uname

from hpyutils.ticker import Ticker
from hpyutils.singleton import Singleton
from utils.render_bpy import RenderTask, BpyScriptor

from json import loads
from hashlib import md5 

from GPUtil import getGPUs
from requests import get, post


# 分解测试这些接口，尤其是下载到渲染的这段。


@Singleton
class MetaBehavior():
    '''
    This is the main class for farmer worker.
    Use self.status==0 to flag free and 1 for in rendering.
    '''
    def __init__(self, config_path='config.json'):
        self.counter = 0
        self.username = None
        self.password = None
        self.host = None
        self.port = None
        self.lock = Lock()
        # With self.status -- 0: free, 1: in rendering, 2: render finish.
        self.status = 0
        self.interval = 0.2
        self.render = BpyScriptor()
        self.read_config(config_path)
        self.worker_name = f'{self.username}@{uname().node}'
        self.current_task = None
        t = Ticker()
        t.register(self)


    def run_worker(self):
        '''
        Begin event loop.
        '''
        print('Work, work~')
        while True:
            if self.status == 0:
                self.get_one_task()
            if self.status == 1:
                self.submit_one_task()
            sleep(self.interval)
        

    def set_task(self, task=None):
        '''
        Set current task before render and reset to None when render finishes.
        '''
        with self.lock:
            self.status = task == None
            self.current_task = task
        return


    def read_config(self, config_path):
        '''
        Server host, port, username, password etc., are included.
        '''
        self.host = 'localhost'
        self.port = '5000'
        self.username = 'hatuki'
        self.password = '114514'
    

    def get_one_task(self):
        url = f'http://{self.host}:{self.port}/api/get-one-task/{self.worker_name}'
        res = get(url)
        data = loads(res.content)
        print(data)
        # If interrupted and restarted, submit the last task as failed.
        if 'code' in data and 'with_bpy' in data:
            if data['code'] == 2:
                self.submit_one_task({'code': 2})
                return
            if data['code'] == 0:
                with self.lock:
                    self.status = 1
                if data['with_bpy']:
                    self.render.run_bpy(data['d_link'], data['d_md5'])
                else:
                    self.render.render_single(data['d_link'], data['d_md5'])
        return 


    def submit_one_task(self, data):
        '''
        Code -- 0: finish, 1: file corrupted, 2: interrupted. 
        '''
        # 1. Upload file.
        # 2. Send GET request with task token.
        # 3. Set status code to 0.
        url = f'http://{self.host}:{self.port}/api/submit'
        if 'code' in data and data['code'] == 0:
            # Upload file first.
            if 'with_bpy' in data:
                file = None
                if data['with_bpy']:
                    file = open('blend/outputs.zip')
                else:
                    file = open('output.png')
                post(url, files={'file': file})
            # Post finish then (reuse available).
        post(url, json=data)
        return

    
    def heartbeat(self):
        url = f'http://{self.host}:{self.port}/api/heartbeat'
        data = {
            'worker_name': self.worker_name,
            'status': 0,
            'gpu-status': [{
                'gpu-id': gpu.id,
                'gpu-name': gpu.name,
                'gpu-load': gpu.load,
                'vram-used': gpu.memoryUsed,
                'vram-total': gpu.memoryTotal,
                'gpu-temperature': gpu.temperature
            } for gpu in getGPUs()]
        }
        res = post(url, json=data)
        return res

    def tick(self):
        self.heartbeat()


if __name__ == '__name__':
    print(os.__name__)