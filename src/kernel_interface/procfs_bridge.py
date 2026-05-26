import os

def read_from_kernel():
    signal_file = "/tmp/vitalis_signal"
    if os.path.exists(signal_file):
        with open(signal_file, "r") as f:
            data = f.read().strip()
        os.remove(signal_file)
        return data
    return "STATUS: NOMINAL"

def send_to_kernel(state_report):
    if "IDLE" not in state_report and "SILENT" not in state_report:
        print(f"[KERNEL_BRIDGE]: {state_report}")
