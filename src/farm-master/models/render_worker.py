# def set_worker(self, worker)

class BlenderWorker():
    def __init__(self):
        self.name = None
        self.is_busy = False
        self.last_alive = None
        self.device_info = None