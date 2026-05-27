import torch
import torch.nn as nn
import torch.nn.functional as F

class DynamicGateAttention(nn.Module):
    def __init__(self, d_model):
        super().__init__()
        self.d_model = d_model
        self.gate_proj = nn.Linear(d_model, 1) # Learns to gate
        self.q = nn.Linear(d_model, d_model)
        self.k = nn.Linear(d_model, d_model)
        self.v = nn.Linear(d_model, d_model)

    def forward(self, x):
        B, T, D = x.shape
        gate = torch.sigmoid(self.gate_proj(x)) # [B, T, 1]
        q, k, v = self.q(x), self.k(x), self.v(x)
        attn = torch.bmm(q, k.transpose(1, 2)) / (D ** 0.5)
        # Apply binary mask via gate
        mask = (gate > 0.5).float()
        attn = attn * mask
        return torch.bmm(F.softmax(attn, dim=-1), v)
