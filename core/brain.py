import time
from core.thinker import emit_thought
from core.nexus import route_thought
from core.ledger import VitalisLedger

class VitalisBrain:
    def __init__(self):
        self.state = "aware"
        self.cycle = 0
        self.last_input = None
        self.ledger = VitalisLedger()
        if not self.ledger.verify_ledger():
            raise Exception("!!! CRITICAL INTEGRITY FAILURE !!!")

    def process(self, input_data):
        self.cycle += 1
        self.last_input = input_data
        if not input_data or input_data.strip() == "":
            response = "IDLE: No input received"
        else:
            response = f"INPUT_RECEIVED: {input_data}"
        
        self.ledger.write_entry("process_cycle", {"cycle": self.cycle, "input": input_data})
        emit_thought(response)
        route_thought({"cycle": self.cycle, "input": input_data, "response": response})
        return response

    def status(self):
        return {"state": self.state, "cycle": self.cycle, "timestamp": time.time()}
