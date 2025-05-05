import json
import pandas as pd 
import subprocess as sp
nodes = sp.run(["kubectl", "get", "nodes", "-o", "json"], capture_output=True, text=True, check=True)
nodes_json = json.loads(nodes.stdout)
with open("sample.json","w") as f:
    json.dump(nodes_json, f, indent=2)
data = []
for i in nodes_json["items"]:
    name = i["metadata"]["name"]
    labels = i["metadata"].get("labels", {})
    capacity = i["status"]["capacity"]
    allocatable = i["status"]["allocatable"]

    status = next((s["type"] for s in i["status"]["conditions"] if s["status"] == "True" and s["type"] == "Ready"), "NotReady")
    cpu = capacity.get("cpu", "None")
    memory = capacity.get("memory", "None")
    pods = capacity.get("pods", "None")
    gpu = capacity.get("nvidia.com/gpu", "0")
    mig_partition = labels.get("cloud.google.com/gke-gpu-partition-size", None)
    mig_enabled = bool(mig_partition)
    time_sharing = labels.get("cloud.google.com/gke-gpu-sharing-strategy") == "time-sharing"
    # print(name, status, cpu, memory, pods, gpu, mig_enabled,time_sharing)
    data.append([name, status, cpu, memory, pods, gpu, mig_enabled,time_sharing])

kubernetes_df = pd.DataFrame(data, columns=["name","status","cpu","memory","pods","gpu","mig_enabled","time_sharing"])
kubernetes_df.to_csv("kubernetes.csv")

