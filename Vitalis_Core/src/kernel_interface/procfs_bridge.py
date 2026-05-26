import os
import fcntl

SHADOW_FILE = "/home/droid/vitalis_core/vitalis_shadow"

def send_to_kernel(data):
    try:
        with open(SHADOW_FILE, "w") as f:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            f.write(data)
            fcntl.flock(f, fcntl.LOCK_UN)
    except:
        pass

def read_from_kernel():
    try:
        with open(SHADOW_FILE, "r") as f:
            return f.read()
    except:
        return "KERNEL_SILENT"
