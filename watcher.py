import os
import sys
import time
import json
import urllib.request

WATCH_DIR = os.path.join(os.getcwd(), "storage/knowledge")
API_URL = "http://127.0.0.1:5000/api/ingest"

def compute_directory_snapshot(target_directory):
    """Generates an absolute structural state index based on file modification timestamps."""
    snapshot = {}
    if not os.path.exists(target_directory):
        return snapshot
        
    for root, _, files in os.walk(target_directory):
        for filename in files:
            # Bypass system manifest layers to prevent tracking recursion loops
            if filename in ["chunks_manifest.json", "vectors_cache.pt"]:
                continue
            file_path = os.path.join(root, filename)
            try:
                snapshot[file_path] = os.path.getmtime(file_path)
            except OSError:
                continue
    return snapshot

def signal_hot_ingestion():
    """Dispatches an internal loopback network signal to trigger zero-downtime vector compilation."""
    payload = json.dumps({"directory": "storage/knowledge"}).encode('utf-8')
    req = urllib.request.Request(
        API_URL, 
        data=payload, 
        headers={'Content-Type': 'application/json'}, 
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            print(f"[+] Daemon: Matrix re-compilation complete. Active Nodes: {res_data.get('active_nodes')}")
    except Exception as e:
        print(f"[-] Daemon: Integrity signal delivery failed. Target endpoint error: {str(e)}")

def start_daemon_loop():
    print(f"[*] Initializing Sovereign File-Watcher Daemon tracking: {WATCH_DIR}")
    last_known_state = compute_directory_snapshot(WATCH_DIR)
    
    while True:
        try:
            time.sleep(3)  # Low-overhead 3-second evaluation cycles
            current_state = compute_directory_snapshot(WATCH_DIR)
            
            if current_state != last_known_state:
                print("[*] Daemon: File-system mutation detected inside secure knowledge vault.")
                signal_hot_ingestion()
                last_known_state = current_state
        except KeyboardInterrupt:
            print("\n[*] Terminating File-Watcher Daemon safely.")
            sys.exit(0)
        except Exception as e:
            print(f"[!] Daemon Runtime Exception: {str(e)}")
            time.sleep(5)

if __name__ == "__main__":
    start_daemon_loop()
