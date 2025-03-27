import bpy
import sys
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"

file = argv[0]
ratio = argv[1]

# print('file', file)
path = file.split('.')[-2]
type = file.split('.')[-1]

for obj in bpy.data.objects:
    if obj.type == "MESH":
        bpy.data.objects.remove(obj)

if type == 'glb':
    bpy.ops.import_scene.gltf(filepath=file)
    bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)    
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            if bpy.context.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles() 
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.select_mode(type = 'FACE')
            bpy.ops.mesh.select_interior_faces()
            bpy.ops.mesh.delete(type='FACE')
            bpy.ops.object.mode_set(mode='OBJECT')


            obj.modifiers.new("Dec",type = "DECIMATE")
            obj.modifiers["Dec"].decimate_type = 'COLLAPSE'

            obj.modifiers["Dec"].ratio = float(ratio)
            bpy.ops.object.modifier_apply(modifier = "Dec")
            bpy.ops.export_scene.gltf(filepath=f'./output/{file.split("/")[-1]}', export_format="GLB")
            bpy.data.objects.remove(obj)

