import json
from datetime import datetime

def format_telemetry(fe, event_name, metadata=None):
    packet = {
        "ts": datetime.utcnow().isoformat(),
        "free_energy": fe.free_energy,
        "event": event_name
    }
    if metadata:
        packet.update(metadata)
    return packet
