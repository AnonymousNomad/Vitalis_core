from core.thinker import emit_thought
from core.nexus import route_thought
import time

class VitalisBrain:
    def __init__(self):
        self.state = "aware"
        self.cycle = 0
        self.last_input = None

    def process(self, input_data):
        self.cycle += 1
        self.last_input = input_data
        if not input_data or input_data.strip() == "":
            response = "IDLE: No input received"
        elif any(w in input_data.lower() for w in ["help", "what", "how", "who"]):
            response = f"QUERY_DETECTED: {input_data}"
        elif any(w in input_data.lower() for w in ["train", "learn", "teach"]):
            response = f"TRAINING_SIGNAL: {input_data}"
        else:
            response = f"INPUT_RECEIVED: {input_data}"
        emit_thought(response)
        route_thought({"cycle": self.cycle, "input": input_data, "response": response})
        return response

    def status(self):
        return {"state": self.state, "cycle": self.cycle, "timestamp": time.time()}

    def analyze_security_threat(self, signal):
        """Advanced heuristic threat analysis layer."""
        if "SYN_FLOOD" in signal:
            return "ACTION: NULL_ROUTE_IP"
        elif "ROOT_ACCESS_UNAUTHORIZED" in signal:
            return "ACTION: TERMINATE_PROCESS_AND_ALERT"
        return "STATUS: NORMAL"
