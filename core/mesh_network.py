import socket
import json

class MeshNode:
    def __init__(self, port=8080):
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def broadcast_thought(self, thought_data):
        """Broadcast cognitive state to other FSI nodes."""
        try:
            self.socket.connect(('localhost', self.port))
            self.socket.send(json.dumps(thought_data).encode())
            self.socket.close()
        except Exception as e:
            return f"Node Offline: {e}"
