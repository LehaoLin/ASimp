import os
import pandas as pd
from torch.utils.data import Dataset
from pytorch3d.io import IO
from pytorch3d.io.experimental_gltf_io import MeshGlbFormat
import numpy as np
from pytorch3d.structures import Meshes, join_meshes_as_batch
from pytorch3d.ops import  sample_points_from_meshes, convert_pointclouds_to_tensor
import torch

def scale_norm(mesh):
    verts = mesh.verts_packed()
    N = verts.shape[0]
    center = verts.mean(0)
    scale = max((verts - center).abs().max(0)[0])
    mesh.offset_verts_(-center)
    mesh.scale_verts_((1.0 / float(scale)))
    return mesh

def ensure_directory_exits(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

point_size = 100000

df = pd.read_csv('./result.csv')
names = list(df['Name'])

ensure_directory_exits('pointclouds')

io = IO()
io.register_meshes_format(MeshGlbFormat())
meshes = []
edges = []
for (idx, name) in enumerate(names):
    model_path = os.path.join(f'./3Ds/{name}.glb')

    mesh = io.load_mesh(model_path, include_textures=False)
    mesh = scale_norm(mesh)
    
    samples = sample_points_from_meshes(mesh, point_size, return_normals=False)
    # print(samples)
    # break

    torch.save(samples, f'./pointclouds/{name}.pt')
    print(name, 'loaded')
    # break