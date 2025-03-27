import os

def simp(file, ratio):
    os.system(f'sudo WAYLAND_DISPLAY=""  blender -b --python blender_script.py -- {file} {ratio}')
    return file