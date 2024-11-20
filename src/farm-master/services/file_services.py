from utils.singleton import Singleton
from werkzeug.utils import secure_filename
import os


@Singleton
class FileServices():
    def __init__(self):
        pass
        

    def get_file(self, name='test'):
        res = 'blender_files/assets/for_test.blend'
        if name != 'test':
            res = name
        return res 
    
    def upload_file(self, user, tag, file):
        '''
        Check md5?
        '''
        print(os.path.abspath(os.curdir))
        file_name = secure_filename(file.filename)
        print(file.filename)
        file_path = f'blender_files/{user}/{tag}/'
        print(f'{file.filename} is saved at path "{file_path}".')
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file.save(file_path + file_name)
