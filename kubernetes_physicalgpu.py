import subprocess
import re

def get_allocated_gpus():
    result = subprocess.run(
        ["kubectl", "describe", "nodes"],
        capture_output=True,
        text=True,
        check=True
    )
    nodes_output = result.stdout.split("Name: ")
    gpu_data = []
    total_allocated_gpus = 0

    for node_info in nodes_output[1:]:
        lines = node_info.splitlines()
        node_name = lines[0].strip()

        match = re.search(r'nvidia.com/gpu\s+(\d+)\s+(\d+)', node_info)
        if match:
            requested, allocated = map(int, match.groups())
            gpu_data.append((node_name, requested, allocated))
            total_allocated_gpus += allocated

    return total_allocated_gpus, gpu_data

total_gpus, per_node_data = get_allocated_gpus()
print("Total Allocated GPUs (physical count):", total_gpus)
for name, req, lim in per_node_data:
    print(f"  Node: {name} | Requested={req}, Allocated={lim}")
