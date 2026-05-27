import torch

class NeuralDiagnostic:
    @staticmethod
    def inspect_layer(tensor, label="Layer"):
        """Print activation metrics to the terminal."""
        mean_act = tensor.mean().item()
        std_act = tensor.std().item()
        print(f"[DIAGNOSTIC] {label} | Mean: {mean_act:.4f} | Std: {std_act:.4f}")

    @staticmethod
    def visualize_gate(gate_tensor):
        """Binary representation of active gates in DGA."""
        active_count = (gate_tensor > 0.5).sum().item()
        print(f"[DIAGNOSTIC] DGA Active Gates: {active_count}")
