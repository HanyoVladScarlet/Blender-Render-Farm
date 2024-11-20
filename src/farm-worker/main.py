import requests
import time
import random
import os
from datetime import datetime as dt


def main():
    ''''''
    worker_name = f'worker-{os.getpid()}'
    # Flag the first entry.
    flag = False
    finished = True
    start = float('inf')
    consumption = 1 + random.random() * 3
    while True:
        try:
            status_data = heartbeat(worker_name, 0 if finished else 1)
            # Status report.
            res = requests.post('http://localhost:5000/api/heartbeat',  json=status_data)
            print(res.content)

            if finished:
                if flag:
                    # Submit one task
                    data = {'worker_name': worker_name, 'res':  'finished'}
                    res = requests.post('http://localhost:5000/api/submit-one-task', json=data)
                # Get one task
                res = requests.get(f'http://localhost:5000/api/get-one-task/{worker_name}')
                print(res.content)
                start = time.time()
                consumption = 1 + random.random() * 3

            finished = time.time() - start > consumption
        except Exception as e:
            print(e)
        time.sleep(0.3)
        flag = True


def heartbeat(worker_name, status):
    data = {
        'worker_name': worker_name,
        'worker_data': {
            'status': status
        }
    }
    return data

if __name__ == '__main__':
    main()