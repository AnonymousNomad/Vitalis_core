import math

class FreeEnergyEngine:
    def __init__(self, alpha=0.85):
        self.alpha = alpha
        self.free_energy = 0.0

    def ingest_observation(self, surprisal):
        self.free_energy = (self.alpha * self.free_energy + (1.0 - self.alpha) * surprisal)

    def temperature_factor(self, base_temp=0.8):
        factor = 1.0 + 0.5 * math.tanh(self.free_energy - 1.0)
        return max(0.4, min(1.4, base_temp * factor))
