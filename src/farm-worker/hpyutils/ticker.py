from threading import Thread, Lock
from hpyutils.singleton import Singleton
from time import sleep, time_ns


@Singleton
class Ticker():
    '''
    Use singleton with method ticker.
    Note the object registered to Ticker must have a method named `tick` with no params and return.
    '''
    def __init__(self):
        self.lock = Lock()
        self.pause = False
        self.fps = 64
        self.registered_instances = []
        self.main_thread = Thread(target=self.tick, name='ticker-main-thread', daemon=True)
        self.main_thread.start()

    def register(self, target):
        '''
        Note the object registered to Ticker must have a method named `tick` with no params and return.
        '''
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
        last = 0
        while not self.pause:
            if time_ns() - last < 1_000_000_000 / self.fps:
                continue
            for ins in self.registered_instances:
                try:
                    ins.tick()
                except Exception as e:
                    print(e)
            last = time_ns()
        return
