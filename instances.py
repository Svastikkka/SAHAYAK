import json
import subprocess as sp
import pandas as pd
instances = sp.run(["gcloud", "compute", "instances", "list", "--project=nonprod1-svc-r4rc", "--format=json"],capture_output=True,text=True,check=True)
# instances = sp.run(["gcloud", "compute", "instances", "list", "--project=nonprod1-svc-r4rc", "--format=json"],check=True)
# instances_json = json.loads(instances.stdout)
# 
# with open("sample.json","w") as f:
#   json.dump(instances_json,f,indent=2)
#     
instances_json = json.loads(instances.stdout)
ram_lookup = {
    "a2-ultragpu-1g": "85 GB",
    "a2-ultragpu-2g": "85 GB",      # Assuming same as a2-ultragpu-1g for now
    "c2-standard-16": "64 GB",      # c2-standard-16 typically comes with 64 GB
    "e2-medium": "4 GB",            # e2-medium has 4 GB RAM
    "g2-standard-48": "192 GB",     # g2-standard-48 typically comes with 192 GB RAM
    "n1-highmem-8": "52 GB",        # n1-highmem-8 comes with 52 GB RAM
    "a2-highgpu-1g": "85 GB",       # Assuming same as a2-ultragpu-1g for now
    "custom-2-12288": "12 GB",      # custom-2-12288 has 12 GB RAM
    "e2-standard-4": "16 GB",       # e2-standard-4 comes with 16 GB RAM
    "g2-custom-4-32768": "32 GB",   # g2-custom-4-32768 comes with 32 GB RAM
    "n1-standard-1": "3.75 GB",     # n1-standard-1 has 3.75 GB RAM
    "n1-standard-4": "15 GB",       # n1-standard-4 has 15 GB RAM
    "e2-small": "2 GB",             # e2-small has 2 GB RAM
}
data = []
for i in instances_json:
    name = i.get("name")
    zone = i.get("zone", "").split("/")[-1]
    status = "STOPPED" if i.get("status") == "TERMINATED" else i.get("status")
    machine_type = i.get("machineType", "").split("/")[-1]
    internal_ip = i.get("networkInterfaces", [{}])[0].get("networkIP", "")
    external_ip = i.get("networkInterfaces", [{}])[0].get("accessConfigs", [{}])[0].get("natIP", "")
    # labels = i.get("labels", {})
    cpu = i.get("cpuPlatform", "Unknown CPU")
    ram = ram_lookup.get(machine_type,"UNKNOWN")
    gpu_info = i.get("guestAccelerators", [])
    gpu_count = gpu_info[0].get("acceleratorCount", 0) if gpu_info else 0
    gpu_type = str(gpu_info[0].get("acceleratorType", "")).split("/")[-1] if gpu_info else "None"
    disks =i.get("disks")[0].get("deviceName")
    disks_size =i.get("disks")[0].get("diskSizeGb")

    # print(name,zone,status,machine_type,internal_ip,external_ip,cpu,ram,gpu_type,gpu_count,disks,disks_size+"GB")
    data.append([name,zone,status,machine_type,internal_ip,external_ip,cpu,ram,gpu_type,gpu_count,disks,disks_size])

instances_df = pd.DataFrame(data,columns=["Name", "Zone", "Status", "Machine Type", "Internal IP", "External IP", "CPU", "RAM", "GPU Type", "GPU Count","Disk","DiskSizeGB"])
instances_df.to_csv("instances.csv")
print(instances_df["GPU Count"].groupby(instances_df["GPU Type"]).sum())
