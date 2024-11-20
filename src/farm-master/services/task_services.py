from datetime import datetime as dt
from uuid import uuid4 as uuid
# from mathutils import Vector

import numpy as np
from repositories.task_repository import TaskDispatcher
from utils.singleton import Singleton


@Singleton
class TaskServices():
    '''
    Use singleton with method task_services.
    '''    
    def __init__(self):
        self.td = TaskDispatcher()

    def get_one_task(self, worker_name):
        return self.td.get_one_task(worker_name)
    
    def submit_one_task(self, data):
        return self.td.submit_one_task(data)
    
    def heartbeat(self, data):
        return self.td.heartbeat(data)


# class TaskScheduler():
#     def __init__(self, distribution=None, max_count=5):
#         # Use default asset path.
#         self.distribution = distribution
#         self.max_count = max_count
#         self.squence = np.random.normal(size=(max_count, max_count))
#         self.squence[:, 0] *= 2
#         # Following list are mapped to ground truths.
#         self.image_hash = [uuid() for i in range(self.max_count)]
#         # for i in range(max_count):
#         #     self.image_hash.append(uuid1())
#         self.scene_presets = np.random.random_integers(low=0, high=9, size=(max_count))
#         self.camera_setups = []
        
#         pass

#     def create_task(self, image_count=10, distribution=None):
#         res = {}
#         res['distribution'] = distribution
#         res['series_info'] = {
#             'time_stamp': dt.now().timestamp()
#         }
#         res['images'] = []
#         for i in range(image_count):
#             res['images'].append({
#                 uuid(): {
#                     'scene_setups': {

#                     },
#                     'degraded': []
#                 } 
#             })

#     def run(self):
        
#         self.current += 1
         

#     def get_degraded(self):
#         '''Get one of the degraded parameters'''
#         res = {}
            
#         return res
    
#     def get_tags(self):
#         res = {}
#         return res
    
# if __name__ == '__main__':
#     from matplotlib import pyplot as plt
#     g = TaskScheduler(max_count=500)
#     # print(g.squence)
#     print(g.scene_presets)
#     print(g.image_hash)
#     x = np.zeros((g.max_count))
#     y = np.zeros((g.max_count))
#     for i in range(g.max_count):
#         x[i] = g.squence[i][0]
#         y[i] = g.squence[i][1]
#     plt.scatter(x, y)
#     plt.show()