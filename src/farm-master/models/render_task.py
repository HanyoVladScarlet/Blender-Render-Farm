# class TaskTemplate():
class RenderTask():
    def __init__(self):
        self.token = None
        self.username = 'anonymous'
        self.tag = 'demo-tag'
        self.timestamp = 0
        self.filename = 'blend.zip'

    def set_token(self, token):
        self.token = token
        return self