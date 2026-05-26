import os

def read_from_kernel():
    # Check for injected signals first
    signal_file = "/tmp/vitalis_signal"
    if os.path.exists(signal_file):
        with open(signal_file, "r") as f:
            data = f.read().strip()
        os.remove(signal_file) # Consume the signal
        return data
    return "STATUS: NOMINAL"

def send_to_kernel(state_report):
    # Standard output for logging purposes
    print(f"[KERNEL_BRIDGE]: {state_report}")
