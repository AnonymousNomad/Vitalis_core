import time, os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.core.watchdog import update_manifest
from src.core.memory_engine import MemoryEngine

class VaultHandler(FileSystemEventHandler):
    def __init__(self):
        self.engine = MemoryEngine()
        
    def on_modified(self, event):
        if event.src_path.endswith(".txt"):
            print(f"[*] Change detected in {event.src_path}. Re-signing manifest & Hot-ingesting...")
            update_manifest()
            self.engine.ingest_knowledge() # Re-builds local FAISS tensors
            print("[+] Hot-ingestion complete. System secure.")

if __name__ == "__main__":
    if not os.path.exists("storage/knowledge/manifest.sha256"):
        update_manifest()
    
    observer = Observer()
    observer.schedule(VaultHandler(), path='storage/knowledge', recursive=False)
    observer.start()
    print("[*] FSI Hot-Ingestion Daemon Active. Watching storage/knowledge...")
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
