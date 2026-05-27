import torch
import torch.nn as nn

class MetaLearningOptimizer(nn.Module):
    def __init__(self, input_dim=4):
        super().__init__()
        # Input: [free_energy, avg_hidden, temp, cycle_ratio]
        self.net = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )

    def forward(self, fe_stats):
        # Predicts multiplier [0.0, 1.0] to scale the base LR
        return self.net(fe_stats)
