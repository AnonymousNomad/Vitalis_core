import sys
import subprocess

# 1. Force installation before any imports occur
try:
    import faiss
except ImportError:
    print("Installing faiss-cpu...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "faiss-cpu"])
    import faiss

# 2. Now it is safe to import your engine
from src.core.memory_engine import MemoryEngine

if __name__ == "__main__":
    print("Engine initialized successfully.")
