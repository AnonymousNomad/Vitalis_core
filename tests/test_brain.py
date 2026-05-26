import sys
import os
sys.path.insert(0, os.path.expanduser("~/vitalis_cybercore"))

from core.brain import VitalisBrain, BrainResponse

def test_high_threat():
    brain = VitalisBrain()
    resp = brain.process("malware detected on host")
    assert resp.severity == "HIGH"
    assert "malware" in resp.tags
    print("PASS: high threat")

def test_defensive():
    brain = VitalisBrain()
    resp = brain.process("monitor the firewall")
    assert resp.severity == "INFO"
    print("PASS: defensive action")

def test_unknown():
    brain = VitalisBrain()
    resp = brain.process("just a random sentence")
    assert resp.severity == "NONE"
    print("PASS: unknown input")

if __name__ == "__main__":
    test_high_threat()
    test_defensive()
    test_unknown()
    print("All tests passed.")
