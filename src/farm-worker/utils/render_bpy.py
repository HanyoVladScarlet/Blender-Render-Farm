import os
from importlib import import_module

import bpy
from requests import get
from hashlib import md5 
from zipfile import ZipFile


class RenderTask():
    def __init__(self):
        self.token = None
        self.tag = None
        self.with_bpy = None
        self.md5_code = None


class BpyScriptor():
    '''
    It doesn't matter if there are multiple BpyScriptors.
    '''
    def run_bpy(self, d_link, d_md5, unzip=True):
        '''
        It is agreed that the downloaded files are structured as demanded, referring to Readme.md
        '''
        try: 
            # 1. Check if there is an existed file share the same md5 code with the file to be downloaded.
            with open('blend.zip', 'wb') as f:
                f.write(response.content)
                md5_res = md5(f.read()).hexdigest()
                if md5_res == d_md5:
                    response = get(d_link)
                # By Microsoft Copilot.
                if unzip:
                    os.makedirs('blend', exist_ok=True)
                    with ZipFile('blend.zip', 'r') as f:
                        f.extractall('blend')
            print('Unzip successfully.')
            module_name = 'blend.main'
            blend_main = import_module(module_name)
            curdir = os.curdir
            os.chdir('blend')
            blend_main.main()
            os.chdir(curdir)
        except Exception as e:
            print(e)

    def render_single(self, d_link, md5_code):
        '''
        For single image rendering, all information needed is set in `.blend` file.
        Do not change anything, except those in CYCLES preferences.
        '''
        file_path = 'online-cache/main.blend'
        with open(file_path, 'wb') as f:
            md5_res = md5(f.read()).hexdigest()
            if md5_res != md5_code:
                response = get(d_link)
                f.write(response.content)
        bpy.ops.wm.open_mainfile(filepath=file_path)
        self.set_cycles()        
        bpy.ops.render.render()
        bpy.data.images['Render Result'].save_render('output.png')
        return
    
    def set_cycles(self):
        '''
        DO NOT ASSIGN RENDER ENGINE.
        '''
        # Note that an opened scene is of necessity for modifying these options.
        # Not omittable.
        bpy.context.preferences.addons["cycles"].preferences.get_devices()
        # OPTIX is faster than CUDA.
        bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'OPTIX'
        for device in bpy.context.preferences.addons['cycles'].preferences.devices:
            if 'nvidia' in device.name.lower():
                device.use = True
                print(device.name)
                print(device)
        bpy.context.scene.cycles.device = 'GPU'
        # Make this adaptive.
        print(bpy.context.preferences.addons['cycles'].preferences.compute_device_type)


if __name__ == '__main__':
    pass