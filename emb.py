import torch
import os
import pandas as pd

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
df = pd.read_csv('./data.csv')
names = list(df['Name'])


for name in names:
    print(name)
    for i in [20]:
        print(i)
        data = torch.load(f'./pointclouds/{name}.pt')[0].tolist()
        data = torch.tensor([data])

        data = data.to(device)
        model = torch.load(f"./ae-model/model.pth", map_location=device)
        model = model.to(device)
        model.eval()

        with torch.no_grad():  # no need to calculate gradients, as we are not training the model
            output_tensor = model.encoder(data.permute(0,2,1))
            output_tensor = output_tensor.to('cpu')
            torch.save(output_tensor, f'./emb-{i}/{name}.pt')