import torch
from core.fluid_transformer import FluidTransformer

class SyncManager:
    def __init__(self, vocab_size=256):
        self.heads = [FluidTransformer(vocab_size) for _ in range(3)]

    def forward(self, input_ids):
        # Consensus: Average logits across all three heads
        logits_list = [h(input_ids) for h in self.heads]
        return sum(logits_list) / len(logits_list)
