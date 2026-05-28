import os
import sys
import json
import torch
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class LocalRetrievalEngine:
    def __init__(self, model_name="all-MiniLM-L6-v2", storage_dir="storage/knowledge"):
        from sentence_transformers import SentenceTransformer
        self.embedder = SentenceTransformer(model_name)
        self.storage_dir = os.path.join(os.getcwd(), storage_dir)
        self.manifest_path = os.path.join(self.storage_dir, "chunks_manifest.json")
        self.vectors_path = os.path.join(self.storage_dir, "vectors_cache.pt")

    def _load_memory_vault(self):
        """Loads local tensor arrays and structural manifests from the sovereign database."""
        if not os.path.exists(self.manifest_path) or not os.path.exists(self.vectors_path):
            print("[-] Retrieval Warning: Memory vault matrix files do not exist on disk yet.")
            return None, None
            
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        vectors = torch.load(self.vectors_path, map_location='cpu')
        return manifest, vectors

    def query(self, query_string, top_k=3, temporal_ceiling=None):
        """Vectorizes user query offline and extracts the highest-affinity contextual matches."""
        manifest, vectors = self._load_memory_vault()
        if manifest is None or vectors is None:
            return []

        # Step 1: Compute query vector locally
        query_vector = self.embedder.encode(query_string, convert_to_tensor=True, show_progress_bar=False).cpu()

        # Step 2: Compute exact cosine similarities across the stacked tensor array
        similarities = torch.nn.functional.cosine_similarity(vectors, query_vector.unsqueeze(0), dim=1)

        # Step 3: Apply Temporal Constraints if active
        if temporal_ceiling is not None:
            valid_indices = [
                idx for idx, chunk in enumerate(manifest)
                if chunk.get('timestamp', 0) <= temporal_ceiling
            ]
        else:
            valid_indices = list(range(len(manifest)))

        if not valid_indices:
            return []

        # Isolate scores matching structural boundaries
        filtered_similarities = similarities[valid_indices]
        
        # Step 4: Extract top-K coordinate coordinates
        actual_k = min(top_k, len(filtered_similarities))
        top_results = torch.topk(filtered_similarities, actual_k)

        matched_context = []
        for score, local_idx in zip(top_results.values, top_results.indices):
            actual_manifest_idx = valid_indices[local_idx.item()]
            chunk_data = manifest[actual_manifest_idx].copy()
            chunk_data['score'] = float(score.item())
            matched_context.append(chunk_data)

        return matched_context

if __name__ == "__main__":
    # Internal baseline validation harness
    retriever = LocalRetrievalEngine()
    print("[*] Local Retrieval Subsystem Initialized. Testing internal matrix queries...")
    sample_matches = retriever.query("quantum mechanics psychiatry architecture configuration", top_k=2)
    print(f"[+] Operational Check: Extracted {len(sample_matches)} matches from local database.")
