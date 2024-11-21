from hpyutils.singleton import Singleton
import bpy

@Singleton
class BpyScriptor():
    def __init__(self):
        pass

    def prepare(self):
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


    def render(self, file_path, output_path):
        '''
        For single image rendering, all information needed is set in `.blend` file.
        Do not change anything, except those in CYCLES preferences.
        '''
        bpy.ops.wm.open_mainfile(filepath=file_path)
        self.prepare()        
        bpy.ops.render.render()
        bpy.data.images['Render Result'].save_render(output_path)
        return
