import os
import psutil

class EnvironmentManager:
    def __init__(self):
        self.process = psutil.Process(os.getpid())

    def get_resource_usage(self):
        """Monitor CPU and memory usage to ensure local operation stability."""
        return {
            "cpu_percent": self.process.cpu_percent(interval=1),
            "memory_mb": self.process.memory_info().rss / (1024 * 1024)
        }

    def enforce_constraints(self, max_memory_mb=2048):
        """Emergency throttle if the system exceeds memory limits."""
        usage = self.get_resource_usage()
        if usage["memory_mb"] > max_memory_mb:
            return "THROTTLE_REQUIRED: Memory ceiling reached."
        return "STABLE: Resources within sovereign limits."
