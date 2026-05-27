import os
import json

class MemoryRotator:
    def __init__(self, memory_file="storage/memory.json"):
        self.memory_file = memory_file

    def rotate(self, current_data):
        """Compacts memory to maintain system performance."""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                history = json.load(f)
            # Only retain last 100 cycles
            history = history[-100:]
            history.append(current_data)
            with open(self.memory_file, "w") as f:
                json.dump(history, f)
