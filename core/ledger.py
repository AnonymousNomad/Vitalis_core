import hashlib
import json
import os
from datetime import datetime

class VitalisLedger:
    def __init__(self, filepath="storage/journal.log"):
        self.filepath = filepath
        if not os.path.exists(os.path.dirname(self.filepath)):
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

    def _generate_hash(self, entry):
        return hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()

    def write_entry(self, event_type, data):
        prev_hash = self.get_last_hash()
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event_type,
            "data": data,
            "prev_hash": prev_hash
        }
        entry["hash"] = self._generate_hash(entry)
        with open(self.filepath, "a") as f:
            f.write(json.dumps(entry) + "\n")
        return entry["hash"]

    def get_last_hash(self):
        if not os.path.exists(self.filepath):
            return "0" * 64
        with open(self.filepath, "rb") as f:
            f.seek(0, os.SEEK_END)
            pos = f.tell()
            while pos > 0:
                pos -= 1
                f.seek(pos)
                if f.read(1) == b'\n' and pos != f.tell() - 1:
                    break
            last_line = f.readline().decode().strip()
            if not last_line: return "0" * 64
            return json.loads(last_line)["hash"]

    def verify_ledger(self):
        if not os.path.exists(self.filepath): return True
        prev = "0" * 64
        with open(self.filepath, "r") as f:
            for line in f:
                entry = json.loads(line)
                if entry["prev_hash"] != prev: return False
                prev = entry["hash"]
        return True
