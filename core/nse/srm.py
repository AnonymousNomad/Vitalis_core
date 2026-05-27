import torch
import torch.nn as nn

class SelfReconstructionMemory(nn.Module):
    def __init__(self, d_model, latent_dim=64):
        super().__init__()
        self.encoder = nn.Linear(d_model, latent_dim)
        self.decoder = nn.Linear(latent_dim, d_model)

    def forward(self, x):
        # Compress
        latent = self.encoder(x)
        # Reconstruct
        reconstruction = self.decoder(latent)
        # Store latent as episodic memory
        return reconstruction, latent
