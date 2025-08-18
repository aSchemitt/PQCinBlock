import time
import platform
import cpuinfo
import psutil
import json
import subprocess
from datetime import datetime

def measure_timer_resolution(samples=10_000):
    """Measure the effective resolution of time.perf_counter()."""
    min_diff = float('inf')
    for _ in range(samples):
        t1 = time.perf_counter()
        t2 = time.perf_counter()
        diff = t2 - t1
        if diff > 0:
            min_diff = min(min_diff, diff)
    return min_diff

# def get_gpu_info():
#     """Attempt to get GPU info (if NVIDIA/CUDA is available)."""
#     try:
#         result = subprocess.run(["nvidia-smi", "--query-gpu=name,driver_version", "--format=csv,noheader"], 
#                                capture_output=True, text=True)
#         if result.returncode == 0:
#             return result.stdout.strip()
#     except FileNotFoundError:
#         pass
#     return "Not available"

def collect_system_metadata():
    """Collect all relevant hardware/software metadata."""
    # Timer precision
    timer_resolution_ns = measure_timer_resolution() * 1e9
    
    # CPU
    cpu_info = cpuinfo.get_cpu_info()
    
    # System
    metadata = {
        "timestamp": datetime.now().isoformat(),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
        },
        "python": {
            "version": platform.python_version(),
            "compiler": platform.python_compiler(),
            "implementation": platform.python_implementation(),
        },
        "cpu": {
            "brand": cpu_info.get("brand_raw", "unknown"),
            "cores_physical": psutil.cpu_count(logical=False),
            "cores_logical": psutil.cpu_count(logical=True),
            "hz_advertised": cpu_info.get("hz_advertised_friendly", "unknown"),
            "hz_actual": cpu_info.get("hz_actual_friendly", "unknown"),
            "architecture": cpu_info.get("arch_string_raw", "unknown"),
        },
        "memory": {
            "total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        },
        # "gpu": get_gpu_info(),
        "timer": {
            "perf_counter_resolution_ns": timer_resolution_ns,
            "perf_counter_units": "seconds (float)",
            "time_ns_available": hasattr(time, 'time_ns'),
        },
        "environment": {
            "cpu_governor": get_cpu_governor() if platform.system() == "Linux" else "N/A",
            "cpu_affinity": list(psutil.Process().cpu_affinity()),
        }
    }
    
    return metadata

def get_cpu_governor():
    """Get CPU frequency governor (Linux only)."""
    try:
        with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Unknown"

def export_metadata(format="json", filename=None):
    """Export metadata to file."""
    data = collect_system_metadata()
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"benchmark_metadata_{timestamp}.{format}"
    
    if format == "json":
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
    elif format == "csv":
        import pandas as pd
        flat_data = pd.json_normalize(data, sep="_").to_dict(orient='records')[0]
        pd.DataFrame.from_dict(flat_data, orient="index").to_csv(filename, header=False)
    else:
        raise ValueError("Format must be 'json' or 'csv'")
    
    print(f"Metadata exported to {filename}")
    return filename

# # Example usage
# if __name__ == "__main__":
#     # Print to console
#     print(json.dumps(collect_system_metadata(), indent=2))
    
#     # Export to file (JSON by default)
#     export_metadata()