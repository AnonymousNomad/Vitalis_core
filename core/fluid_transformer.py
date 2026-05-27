import torch
import torch.nn as nn
import math
from core.ledger import VitalisLedger

class FluidTransformer(nn.Module):
    def __init__(self, vocab_size=256, hidden_dim=256):
        super().__init__()
        self.ledger = VitalisLedger()
        self.embed = nn.Embedding(vocab_size, hidden_dim)
        self.layers = nn.ModuleList([nn.TransformerEncoderLayer(d_model=hidden_dim, nhead=8) for _ in range(4)])
        self.head = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x):
        x = self.embed(x)
        for layer in self.layers:
            x = layer(x)
        return self.head(x)
