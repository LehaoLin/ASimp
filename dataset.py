import os
import pandas as pd
from torch.utils.data import Dataset
from pytorch3d.io import IO
from pytorch3d.io.experimental_gltf_io import MeshGlbFormat
import numpy as np
from pytorch3d.structures import Meshes, join_meshes_as_batch
from pytorch3d.ops import  sample_points_from_meshes, convert_pointclouds_to_tensor
import torch

from torch.utils.data import DataLoader, ConcatDataset

    
class CustomDataset(Dataset):
    def __init__(self, names, labels, transform=None, target_transform=None):
        self.names = names
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        pointcloud = torch.load(f'./pointclouds/{self.names[idx]}.pt')
        # return pointcloud, self.labels[idx]
        return pointcloud[0]

def get_dataloaders():
    df_train = pd.read_csv('./sets/train.csv')
    names_train = df_train['Name']
    labels_train = df_train['mean']
    train_datset = CustomDataset(names_train, labels_train)

    df_test = pd.read_csv('./sets/test.csv')
    names_test = df_test['Name']
    labels_test = df_test['mean']
    test_dataset = CustomDataset(names_test, labels_test)

    train_loader = DataLoader(train_datset, shuffle=True, batch_size=16)
    test_loader = DataLoader(test_dataset, shuffle=True, batch_size=16)
    print('dataset complete')
    return train_loader, test_loader


class EmbDataset(Dataset):
    def __init__(self, names, faces, labels, emb_size, transform=None, target_transform=None):
        self.names = names
        self.faces = faces
        self.labels = labels
        self.emb_size = emb_size

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        pure_name = self.names[idx].split('#')[0]
        emb = torch.load(f'./emb-{self.emb_size}/{pure_name}.pt')[0]
        # print(emb, type(emb))
        # print(self.faces[idx]/1000, type(float(self.faces[idx]/1000)))
        input = torch.concat((emb, torch.tensor([np.float32(self.faces[idx]/1000)])), 0)
        return input, np.float32(self.labels[idx])

def emb_dataloaders(emb_size):
    df_train = pd.read_csv('./sets/train.csv')
    names_train = df_train['Name']
    labels_train = df_train['mean']
    faces_train = df_train['faces']

    new_names = []
    new_labels = []
    new_faces = []
    for idx, name in enumerate(names_train):
        diff = round((1- labels_train[idx]/100) * faces_train[idx] / 5)
        new_names.append(f'{name}#1')
        new_faces.append(faces_train[idx] - diff * 0)
        new_labels.append(labels_train[idx])
        new_names.append(f'{name}#2')
        new_faces.append(faces_train[idx] - diff * 1)
        new_labels.append(labels_train[idx] / 100 * faces_train[idx] / (faces_train[idx] - diff * 1) * 100)
        new_names.append(f'{name}#3')
        new_faces.append(faces_train[idx] - diff * 2)
        new_labels.append(labels_train[idx] / 100 * faces_train[idx] / (faces_train[idx] - diff * 2) * 100)
        new_names.append(f'{name}#4')
        new_faces.append(faces_train[idx] - diff * 3)
        new_labels.append(labels_train[idx] / 100 * faces_train[idx] / (faces_train[idx] - diff * 3) * 100)
        new_names.append(f'{name}#5')
        new_faces.append(faces_train[idx] - diff * 4)
        new_labels.append(labels_train[idx] / 100 * faces_train[idx] / (faces_train[idx] - diff * 4) * 100)

    train_datset = EmbDataset(new_names, new_faces, new_labels, emb_size)

    df_test = pd.read_csv('./sets/test.csv')
    names_test = df_test['Name']
    labels_test = df_test['mean']
    faces_test = df_train['faces']

    new_names = []
    new_labels = []
    new_faces = []
    for idx, name in enumerate(names_test):
        diff = round((1- labels_test[idx]/100) * faces_test[idx] / 5)
        new_names.append(f'{name}#1')
        new_faces.append(faces_test[idx] - diff * 0)
        new_labels.append(labels_test[idx])
        new_names.append(f'{name}#2')
        new_faces.append(faces_test[idx] - diff * 1)
        new_labels.append(labels_test[idx] / 100 * faces_test[idx] / (faces_test[idx] - diff * 1) * 100)
        new_names.append(f'{name}#3')
        new_faces.append(faces_test[idx] - diff * 2)
        new_labels.append(labels_test[idx] / 100 * faces_test[idx] / (faces_test[idx] - diff * 2) * 100)
        new_names.append(f'{name}#4')
        new_faces.append(faces_test[idx] - diff * 3)
        new_labels.append(labels_test[idx] / 100 * faces_test[idx] / (faces_test[idx] - diff * 3) * 100)
        new_names.append(f'{name}#5')
        new_faces.append(faces_test[idx] - diff * 4)
        new_labels.append(labels_test[idx] / 100 * faces_test[idx] / (faces_test[idx] - diff * 4) * 100)

    test_dataset = EmbDataset(new_names, new_faces, new_labels, emb_size)

    print(len(train_datset), len(test_dataset))
    print(len(train_datset), len(test_dataset))
    train_loader = DataLoader(train_datset, shuffle=True, batch_size=len(train_datset))
    test_loader = DataLoader(test_dataset, shuffle=True, batch_size=len(test_dataset))
    print('dataset complete')
    return train_loader, test_loader