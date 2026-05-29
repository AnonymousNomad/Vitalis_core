import sqlite3
import numpy as np
import pickle
import os
from .rnn_core import TinyGatedRNN

class VitalisBrain:
    def __init__(self, db_path="sare_ledger.db"):
        self.rnn = TinyGatedRNN()
        self.hidden = np.zeros(self.rnn.hidden_dim)
        self.db_path = db_path
        self.weight_path = "vitalis/data/weights/model.bin"

    def is_trusted(self, concept_id=1):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute("SELECT confidence FROM confidence WHERE concept_id = ?", (concept_id,))
            val = cur.fetchone()
            return val is not None and val[0] >= 0.8
        except:
            return False

    def generate_response(self, text, system_prompt):
        if not self.is_trusted():
            return "THROTTLE_ACTIVE: Insufficient Bayesian confidence."
        
        tokens = [ord(c) % 4000 for c in text]
        for t in tokens:
            _, self.hidden = self.rnn.forward_step(t, self.hidden)
        return "Internal state updated."

    def save_brain(self):
        os.makedirs(os.path.dirname(self.weight_path), exist_ok=True)
        with open(self.weight_path, 'wb') as f:
            pickle.dump(self.rnn.get_weights(), f)
        print("Brain state serialized to disk.")

    def load_brain(self):
        if os.path.exists(self.weight_path):
            with open(self.weight_path, 'rb') as f:
                self.rnn.set_weights(pickle.load(f))
            print("Brain state loaded.")
