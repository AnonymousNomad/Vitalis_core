import subprocess
import sys

# 1. Ensure dependencies are installed
print("Ensuring dependencies...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "faiss-cpu"])

# 2. Import AFTER the installation is guaranteed
from src.core.memory_engine import MemoryEngine

def main():
    engine = MemoryEngine()
    print("Engine initialized successfully.")

if __name__ == "__main__":
    main()
