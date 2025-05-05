import subprocess

def list_disks():
    # Run the gcloud command to list disks with their name, type, size, and users
    result = subprocess.run(
        [
            "gcloud", 
            "compute", 
            "disks", 
            "list", 
            "--format=table(name, type, sizeGb, users)"
        ],
        capture_output=True,
        text=True,
        check=True
    )
    
    # Print the result which contains disk name, type, size, and associated instances (users)
    print("Disks in the project with associated instances:\n")
    print(result.stdout)

if __name__ == "__main__":
    list_disks()
