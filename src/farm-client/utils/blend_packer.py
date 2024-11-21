import os
import sys
from datetime import datetime as dt

import json
import yaml
import zipfile


from requests import post


class BlendPacker():
    def __init__(self, root='./root-folder', force=False, tag_with_time=False):
        self.config = None
        self.root = root
        self.force = force
        self.tag_with_time = tag_with_time
        self.validate()
    
    def validate(self):
        if self.root.endswith('/'):
            self.root = self.root[:-2]
        c_yml = f'{self.root}/config.yml'
        c_json = f'{self.root}/config.json'

        # Load config file.
        # With json on the first and yaml for second.
        if os.path.exists(c_json):
            with open(c_json, 'r') as f:
                self.config = json.load(f)
        elif os.path.exists(c_yml):
            with open(c_yml, 'r') as f:
                self.config = yaml.load(f.read(), Loader=yaml.   FullLoader)
        else:
            raise Exception('Config file does not exist!')


        if 'upload' in self.config and 'with_bpy' in self.config['upload']:
            with_bpy = self.config['upload']['with_bpy']
        else:
            py_init = f'{self.root}/blend/__init__.py'
            py_main = f'{self.root}/blend/main.py'
            py_blend = f'{self.root}/blend/main.blend'
            if os.path.exists(py_init) and os.path.exists  (py_main):
                with_bpy = True
            elif os.path.exists(py_blend):
                with_bpy = False
            else:
                raise Exception('Illegal structure of blend folder!')
        return with_bpy

    def upload(self):
        '''
        Upload options are recorded in config.json.
        {
            "upload": {
                "host": "114.514.19.19",
                "port": "810",
                ...
            },
            ...
        }
        '''
        u_config = self.config['upload']
        host = u_config['host']
        port = u_config['port']

        # Uncomment if you don't need to save network resource.
        # u_config.pop('host')
        # u_config.pop('port')

        # Default settings for convenience.
        # Not recommended for public servers.
        if 'tag' not in u_config:
            u_config['tag'] = 'demo-tag'
        if self.tag_with_time:
            u_config['tag'] += dt.now().strftime('-%Y-%m-%d-%H-%M-%S')
        if 'username' not in u_config:
            u_config['username'] = 'anonymous'

        # Default path for packed zip file.
        file = open('tempo/blend.zip', 'rb') 

        # TODO: Use md5 to check wether the blend file is modified to save network resources.
        is_file_unchanged = True
        url = f'http://{host}:{port}/api/upload/client'

        # Check content.
        print(self.config)
        data = self.config

        response = post(url, json=data) 
        # response = post(url, json=data, files={'blend': file} if is_file_unchanged else {}) 

        if 200 != response.status_code:
            raise Exception
        file.close()

        # Remove temp files, disk strong!
        if 'del_tmp' in u_config and u_config['del_tmp']:
            os.remove('tempo/blend.zip')

        return json.loads(response.content)
    

    def packup(self):
        '''
        This function is to zip blend folder in root folder.
        ''' 
        if not self.force and os.path.exists('tempo/blend.zip'):
            return self

        folder_path = f'{self.root}/blend'
        if not os.path.exists('tempo'):
            os.makedirs('tempo')
        zip_folder(folder_path, 'tempo/blend.zip')

        return self


# By Microsoft Copilot.
def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile. ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath   (file_path, folder_path))
