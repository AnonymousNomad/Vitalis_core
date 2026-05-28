#!/usr/bin/env python3
class FreeEnergyCalculator:
    def __init__(self, alpha=0.85):
        self.alpha = alpha
        self.surprise = 0.0
    def update(self, log_likelihood):
        self.surprise = (self.alpha * self.surprise) + ((1 - self.alpha) * -log_likelihood)
        return self.surprise
