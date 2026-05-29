import sqlite3
import pathlib

class BayesianUpdater:
    THRESHOLD = 0.8
    
    def __init__(self, db_path: pathlib.Path):
        self.db_path = db_path

    def update(self, concept_id: int, success: bool):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT alpha, beta FROM confidence WHERE concept_id = ?", (concept_id,))
            row = cur.fetchone()
            if row:
                alpha, beta = row
                if success:
                    alpha += 1
                else:
                    beta += 1
                
                posterior = alpha / (alpha + beta)
                cur.execute("UPDATE confidence SET alpha = ?, beta = ?, confidence = ? WHERE concept_id = ?", 
                            (alpha, beta, posterior, concept_id))
            conn.commit()
