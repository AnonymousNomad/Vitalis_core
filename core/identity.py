import json
import os

class IdentityManager:
    def __init__(self, identity_file="core/identity.json"):
        self.identity_file = identity_file
        self.identity = self._load_identity()

    def _load_identity(self):
        if os.path.exists(self.identity_file):
            with open(self.identity_file, "r") as f:
                return json.load(f)
        return {"name": "Vitalis", "role": "Synthetic Intelligence", "status": "Sovereign"}

    def get_persona(self):
        return f"{self.identity['name']} (Role: {self.identity['role']})"
