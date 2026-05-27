import json
import os

class EnvLoader:
    def __init__(self, config_path="env.json"):
        self.config_path = config_path
        self.config = self._load()

    def _load(self):
        default_config = {
            "max_memory_mb": 2048,
            "d_model": 256,
            "ledger_path": "storage/ledger.bin",
            "log_level": "DEBUG"
        }
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return json.load(f)
        return default_config

    def get(self, key):
        return self.config.get(key)
