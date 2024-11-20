from threading import Thread, Lock
from utils.singleton import Singleton

Singleton
class Ticker():
    '''
    Use singleton with method ticker.
    '''
    def __init__(self):
        self.lock = Lock()
        self.registered_instances = []

    def register(self, target):
        with self.lock:
            if 'tick' in target.__dir__():
                self.registered_instances.append(target)
            return
    
    def unregister(self, target):
        with self.lock:
            if target in self.registered_instances:
                self.registered_instances.remove(target)
        return        
    
    def tick(self):
        for ins in self.registered_instances:
            try:
                ins.tick()
            except Exception as e:
                print(e.with_traceback())
        return
