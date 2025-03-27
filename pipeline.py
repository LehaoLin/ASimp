import time
import os
import pandas as pd
from torch.utils.data import Dataset
from pytorch3d.io import IO
from pytorch3d.io.experimental_gltf_io import MeshGlbFormat
import numpy as np
from pytorch3d.structures import Meshes, join_meshes_as_batch
from pytorch3d.ops import  sample_points_from_meshes, convert_pointclouds_to_tensor
import torch
from simplify import simp

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
io = IO()
io.register_meshes_format(MeshGlbFormat())
point_size = 100000

def scale_norm(mesh):
    verts = mesh.verts_packed()
    N = verts.shape[0]
    center = verts.mean(0)
    scale = max((verts - center).abs().max(0)[0])
    mesh.offset_verts_(-center)
    mesh.scale_verts_((1.0 / float(scale)))
    return mesh

def run(glb_file):
    start = time.time()
    mesh = io.load_mesh(glb_file, include_textures=False)
    mesh = scale_norm(mesh)
    face_number = len(mesh.faces_list())
    samples = sample_points_from_meshes(mesh, point_size)
    data = samples

    data = data.to(device)
    model = torch.load(f"./ae-model/model.pth", map_location=device)
    model = model.to(device)
    model.eval()
    with torch.no_grad():
        output_tensor = model.encoder(data.permute(0,2,1))

    model = torch.load(f"./mlp-model/model.pth", map_location=device)
    model = model.to(device)
    model.eval()
    input = torch.concat((output_tensor[0], torch.tensor([np.float32(face_number/1000)]).to(device)), 0)
    with torch.no_grad():
        output_tensor = model(input)
        output_tensor = output_tensor.to('cpu')
    ratio = float(output_tensor) / 100
    simp(glb_file, ratio)
    end = time.time()
    process_time = end - start
    return ratio, process_time

names = ['Lion']
names = list(map(lambda x: x.split('.')[0], os.listdir("input")))

time_list = []
for name in names:
    ratio, time_ = run(f'./input/{name}.glb')
    time_list.append(str(time_))
    # print(result)

with open('time.txt', 'w') as f:
    time_record = '\n'.join(time_list)
    f.write(time_record)
