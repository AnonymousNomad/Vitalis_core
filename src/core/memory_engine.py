class MemoryEngine:
    def __init__(self):
        # Perform the import only when the class is instantiated
        import faiss
        print("FAISS loaded successfully.")
        self.faiss = faiss
