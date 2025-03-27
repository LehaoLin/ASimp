import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import Adam
from tqdm import tqdm

from dataset import get_dataloaders
import pandas as pd
from pytorch3d.structures import Meshes
from ae_model import PointCloudAE
from pytorch3d.loss import chamfer_distance # chamfer distance for calculating point cloud distance
import torch.optim as optim
import os


import numpy as np
import random

def add_log(emb_size, ctx):
    with open(f"./loss/loss-{emb_size}.txt", "a") as myfile:
        myfile.write(ctx+'\n')


point_size = 100000
latent_size = [20]


def ensure_directory_exits(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

ensure_directory_exits('loss')
ensure_directory_exits('ae-model')

for latent in latent_size:

    try:
        os.remove(f'./loss/loss-{latent}.txt')
    except:
        pass


    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = PointCloudAE(point_size, latent).to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.0005)

    df = pd.read_csv('./data.csv')
    labels = df['mean']
    names = df['Name']

    train_loader, test_loader = get_dataloaders()

    print('start training')
    num_epochs = 300
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for i, data in enumerate(train_loader):
            optimizer.zero_grad()
            data = data.to(device)
            output = model(data.permute(0,2,1)) # transpose data for NumberxChannelxSize format
            loss, _ = chamfer_distance(data, output) 
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
        epoch_loss = running_loss / len(train_loader)
        print(f"Epoch {epoch+1}/{num_epochs}")
        add_log(latent, f"Epoch {epoch+1}/{num_epochs}")
        print(f"train loss: {epoch_loss}")
        add_log(latent, f"train loss: {epoch_loss}")

        with torch.no_grad():
            test_samples = next(iter(test_loader))
            test_samples = test_samples.to(device)
            output = model(test_samples.permute(0,2,1))
            loss, _ = chamfer_distance(test_samples, output)
            print(f"test loss: {loss}")
            add_log(latent, f"test loss: {loss}")
    
        torch.save(model, f"./ae-model/model-{latent}.pth")
        # break 

    print("Training finished!")