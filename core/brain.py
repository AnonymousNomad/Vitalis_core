import os
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional
import yaml

from core.thinker import emit_thought
from core.nexus import route_thought
from core.threat_logger import ThreatLogger

@dataclass
class BrainResponse:
    status: str
    severity: str
    confidence: float = 0.0
    tags: List[str] = field(default_factory=list)
    payload: str = ""
    cycle: int = 0
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class VitalisBrain:
    def __init__(self, config_path: Optional[Path | str] = None):
        self._config = self._load_config(config_path)
        self.state: str = self._config["brain"]["default_state"]
        self.cycle: int = 0
        self.last_input: Optional[str] = None
        log_path = os.path.expanduser(self._config["brain"]["log_path"])
        self.logger = ThreatLogger(log_path) if self._config["brain"]["enable_logging"] else None
        self._keyword_map: Dict[str, List[str]] = self._build_keyword_map()

    def process(self, input_data: str) -> BrainResponse:
        self.cycle += 1
        self.last_input = input_data
        status_label, severity, tags, confidence = self._classify(input_data.lower())
        response = BrainResponse(
            status=status_label,
            severity=severity,
            confidence=confidence,
            tags=tags,
            payload=input_data,
            cycle=self.cycle
        )
        if self.logger:
            try: self.logger.log(input_data, response.to_dict())
            except Exception as exc: print(f"[ThreatLogger] failed: {exc}")
        try: emit_thought(response.status)
        except Exception as exc: print(f"[emit_thought] error: {exc}")
        try: route_thought(response.to_dict())
        except Exception as exc: print(f"[route_thought] error: {exc}")
        return response

    @staticmethod
    def _load_config(path: Optional[Path | str]) -> Mapping[str, Any]:
        default = {
            "brain": {"default_state": "aware", "enable_logging": True,
                "log_path": "~/vitalis_cybercore/storage/threat_log.jsonl",
                "severity_labels": {"high": "THREAT_DETECTED [HIGH]",
                    "medium": "THREAT_DETECTED [MEDIUM]", "low": "THREAT_DETECTED [LOW]",
                    "info": "DEFENSIVE_ACTION", "train": "TRAINING_SIGNAL",
                    "query": "QUERY_DETECTED", "other": "INPUT_RECEIVED"}},
            "threats": {"high": ["injection","overflow","exploit","payload","malware","breach","ransomware","rootkit"],
                "medium": ["unauthorized","intrusion","attack","vulnerability"],
                "low": ["scan","suspicious","threat","probe"]},
            "defensive": ["monitor","protect","defend","analyze","investigate","audit","patch","harden","firewall"],
            "training": ["train","learn","teach"],
            "query": ["help","what","how","who"]
        }
        if not path:
            path = Path(__file__).with_name("config.yaml")
        try:
            with open(path, "r") as fp:
                external = yaml.safe_load(fp) or {}
            return VitalisBrain._deep_merge(default, external)
        except FileNotFoundError:
            return default

    @staticmethod
    def _deep_merge(base: dict, overlay: dict) -> dict:
        for k, v in overlay.items():
            if isinstance(v, dict) and isinstance(base.get(k), dict):
                base[k] = VitalisBrain._deep_merge(base[k], v)
            else:
                base[k] = v
        return base

    def _build_keyword_map(self) -> Dict[str, List[str]]:
        mapping: Dict[str, List[str]] = {}
        for sev, words in self._config["threats"].items():
            for w in words: mapping.setdefault(w.lower(), []).append(sev)
        for w in self._config["defensive"]: mapping.setdefault(w.lower(), []).append("info")
        for w in self._config["training"]: mapping.setdefault(w.lower(), []).append("train")
        for w in self._config["query"]: mapping.setdefault(w.lower(), []).append("query")
        return mapping

    def _classify(self, lowered: str) -> tuple[str, str, List[str], float]:
        conf_map = {"high": 0.9, "medium": 0.85, "low": 0.7, "info": 0.6, "train": 0.6, "query": 0.5}
        sev_order = ["high", "medium", "low", "info", "train", "query"]
        found: Dict[str, List[str]] = {}
        for word, cats in self._keyword_map.items():
            if word in lowered:
                for cat in cats: found.setdefault(cat, []).append(word)
        for sev in sev_order:
            if sev in found:
                return self._config["brain"]["severity_labels"][sev], sev.upper(), found[sev], conf_map[sev]
        return self._config["brain"]["severity_labels"]["other"], "NONE", [], 0.2
