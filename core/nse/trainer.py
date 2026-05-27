import torch
from core.ledger import VitalisLedger
from core.nse.sync_manager import TripleHeadSyncManager

class NSETrainer:
    def __init__(self, d_model=256):
        self.ledger = VitalisLedger()
        self.model = TripleHeadSyncManager(d_model)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)

    def train_step(self, input_data, fe_stats):
        self.optimizer.zero_grad()
        
        # Consensus pass
        recon, lr_mult = self.model(input_data, fe_stats)
        
        # Loss calculation (e.g., reconstruction error)
        loss = torch.mean((recon - input_data) ** 2)
        loss.backward()
        self.optimizer.step()
        
        # Immutable Ledger Log
        self.ledger.write_entry("training_step", {
            "loss": loss.item(),
            "lr_multiplier": lr_mult.item(),
            "status": "verified_update"
        })
        
        return loss.item()
