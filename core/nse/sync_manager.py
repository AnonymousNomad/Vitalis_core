import torch
import torch.nn as nn
from core.nse.engine import NeuroSynthEngine

class TripleHeadSyncManager(nn.Module):
    def __init__(self, d_model=256):
        super().__init__()
        self.heads = nn.ModuleList([NeuroSynthEngine(d_model) for _ in range(3)])

    def forward(self, x, fe_stats):
        outputs = [head(x, fe_stats) for head in self.heads]
        # Consolidate: Average the reconstructions, Max-pool the LR multipliers
        recons = torch.stack([o[0] for o in outputs]).mean(dim=0)
        lr_multipliers = torch.stack([o[1] for o in outputs]).max(dim=0)[0]
        
        return recons, lr_multipliers
