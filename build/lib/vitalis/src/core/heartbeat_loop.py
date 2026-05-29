import threading
import time
import logging
from vitalis.src.reasoning.bayesian_updater import BayesianUpdater

class HeartbeatLoop(threading.Thread):
    def __init__(self, brain, interval=1.0, db_path="sare_ledger.db"):
        super().__init__(daemon=True)
        self.brain = brain
        self.interval = interval
        self.updater = BayesianUpdater(db_path)
        self.stop_event = threading.Event()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("Heartbeat")

    def run(self):
        self.logger.info(f"Heartbeat loop started (interval={self.interval}s)")
        while not self.stop_event.is_set():
            # 1. Cognitive Pulse
            success = self.brain.pulse()
            
            # 2. Bayesian Update
            # Assuming concept_id 1 is the 'active' focus for this heartbeat
            try:
                self.updater.update(concept_id=1, success=success)
            except Exception as e:
                self.logger.error(f"Updater failed: {e}")
            
            time.sleep(self.interval)

    def stop(self):
        self.stop_event.set()
