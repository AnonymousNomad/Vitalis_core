import json
import os
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

BASE_PATH = Path(os.path.expanduser("~/vitalis_cybercore"))
DEFAULT_LOG = BASE_PATH / "storage" / "threat_log.jsonl"

class ThreatLogger:
    def __init__(self, log_path: Path | str | None = None):
        self.log_path = Path(log_path) if log_path else DEFAULT_LOG
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def log(self, input_data: str, response: Dict[str, Any]) -> None:
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "input": input_data,
            "response": response,
        }
        line = json.dumps(entry, ensure_ascii=False)
        with self._lock, self.log_path.open("a", encoding="utf-8") as fp:
            fp.write(line + "\n")
