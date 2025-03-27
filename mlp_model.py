import torch
import torch.nn as nn
import torch.nn.functional as F


class MLP(nn.Module):
    def __init__(self, emb_size=2):
        super(MLP, self).__init__()
        self.emb_size = emb_size
        self.linear1 = nn.Linear(self.emb_size+1, self.emb_size)
        self.linear2 = nn.Linear(self.emb_size, self.emb_size)
        self.linear3 = nn.Linear(self.emb_size, 1)
        self.prelu = nn.PReLU()
        
    def forward(self, x):
        x = self.linear1(x)
        x = self.prelu(x)
        x = self.linear2(x)
        x = self.prelu(x)
        x = self.linear3(x)
        return x.squeeze(-1)
