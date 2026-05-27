import torch
import torch.nn as nn
from core.nse.dga import DynamicGateAttention
from core.nse.srm import SelfReconstructionMemory
from core.nse.mlo import MetaLearningOptimizer

class NeuroSynthEngine(nn.Module):
    def __init__(self, d_model=256):
        super().__init__()
        self.dga = DynamicGateAttention(d_model)
        self.srm = SelfReconstructionMemory(d_model)
        self.mlo = MetaLearningOptimizer()
        self.norm = nn.LayerNorm(d_model)

    def forward(self, x, fe_stats):
        # 1. Selective Attention
        attn_out = self.dga(x)
        x = self.norm(x + attn_out)
        
        # 2. Episodic Memory Retrieval
        recon, latent = self.srm(x)
        
        # 3. Meta-Optimizer Signal
        lr_multiplier = self.mlo(fe_stats)
        
        return recon, lr_multiplier
