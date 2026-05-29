#!/usr/bin/env python3
from src.core.transformer_wrapper import SovereignTransformer
from src.brain.checkpoint_manager import save_vitalis_weights

class InferenceEngine:
    def __init__(self) -> None:
        self.transformer = SovereignTransformer(model_name="facebook/opt-125m")
        # ... existing core initializations ...

    def export_model(self):
        save_vitalis_weights(self.transformer.model)

    # ... rest of your existing inference methods ...
