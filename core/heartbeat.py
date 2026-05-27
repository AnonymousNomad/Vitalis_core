import time
import threading
from core.ledger import VitalisLedger

class Heartbeat(threading.Thread):
    def __init__(self, fe, interval=1.0):
        super().__init__(daemon=True)
        self.fe = fe
        self.interval = interval
        self.ledger = VitalisLedger()

    def run(self):
        while True:
            telemetry = {"free_energy": self.fe.free_energy}
            self.ledger.write_entry("heartbeat_tick", telemetry)
            time.sleep(self.interval)
