import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import Adam
from tqdm import tqdm
from dataset import emb_dataloaders
import pandas as pd
from pytorch3d.structures import Meshes
from ae_model import PointCloudAE
from mlp_model import MLP
from pytorch3d.loss import chamfer_distance # chamfer distance for calculating point cloud distance
import torch.optim as optim
import os


import numpy as np
import random

def add_log(emb_size, ctx):
    with open(f"./mlploss/loss-{emb_size}.txt", "a") as myfile:
        myfile.write(ctx+'\n')

def ensure_directory_exits(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

ensure_directory_exits('mlploss')
ensure_directory_exits('mlpmodel')

point_size = 100000
latent_size_list = [20]

for latent_size in latent_size_list:
    try:
        os.remove(f'./mlploss/loss-{latent_size}.txt')
    except:
        pass


    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = MLP(latent_size).to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.002)

    criteria = nn.MSELoss()

    df = pd.read_csv('./result.csv')
    labels = df['mean']
    names = df['Name']

    train_loader, test_loader = emb_dataloaders(latent_size)

    print('start training')
    num_epochs = 3000
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for i, data in enumerate(train_loader):
            optimizer.zero_grad()
            inputs, labels = data
            inputs = inputs.to(device)
            labels = labels.to(device)

            output = model(inputs) # transpose data for NumberxChannelxSize format

            loss = criteria(labels, output)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
        epoch_loss = running_loss / len(train_loader)
        print(f"Epoch {epoch+1}/{num_epochs}")
        add_log(latent_size, f"Epoch {epoch+1}/{num_epochs}")
        print(f"train loss: {epoch_loss}")
        add_log(latent_size, f"train loss: {epoch_loss}")

        with torch.no_grad():
            test_samples, labels = next(iter(test_loader))
            
            test_samples = test_samples.to(device)
            labels = labels.to(device)

            output = model(test_samples)
            loss = criteria(labels, output)
            print(f"test loss: {loss}")
            add_log(latent_size, f"test loss: {loss}")

        torch.save(model, f"./mlp-model/model-{latent_size}.pth")
        # break
            

    print("Training finished!")