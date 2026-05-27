import os
import shutil

class KillSwitch:
    def __init__(self, storage_path="storage/"):
        self.storage_path = storage_path

    def trigger(self):
        """Wipe all cognitive snapshots and logs."""
        print("[!] EMERGENCY: INTEGRITY VIOLATION DETECTED. PURGING...")
        if os.path.exists(self.storage_path):
            shutil.rmtree(self.storage_path)
            os.mkdir(self.storage_path)
        print("[!] SYSTEM PURGED. HALTING.")
        exit(1)
