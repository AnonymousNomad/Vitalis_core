import sys
import os
from core.ledger import VitalisLedger
from core.brain import VitalisBrain

def main():
    print("[SYSTEM] Vitalis Core Booting...")
    
    # Initialize Ledger
    ledger = VitalisLedger()
    
    # Cryptographic Integrity Check
    if not ledger.verify_ledger():
        print("[!] CRITICAL: INTEGRITY FAILURE. TAMPERING DETECTED.")
        sys.exit(1)
        
    ledger.write_entry("system_boot", {"status": "verified"})
    
    # Initialize Core
    brain = VitalisBrain()
    print("[SYSTEM] Cognitive Core Synchronized.")
    
    try:
        while True:
            cmd = input(">> ")
            if cmd.lower() == "exit":
                ledger.write_entry("system_shutdown", {"status": "clean"})
                break
            
            response = brain.process(cmd)
            print(f"Vitalis: {response}")
            
    except KeyboardInterrupt:
        ledger.write_entry("system_shutdown", {"status": "interrupt"})
        sys.exit(0)

if __name__ == "__main__":
    main()
