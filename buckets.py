import subprocess

def list_buckets():
    # Run the gcloud command to list buckets with their location and last updated time
    result = subprocess.run(
        [
            "gcloud", 
            "storage", 
            "buckets", 
            "list", 
            "--project=nonprod1-svc-r4rc", 
            "--format=table(name, location, update_time)"
        ],
        capture_output=True,
        text=True,
        check=True
    )
    
    # Print the result which contains bucket name, location, and update time
    print("Buckets in project 'nonprod1-svc-r4rc':\n")
    print(result.stdout)

if __name__ == "__main__":
    list_buckets()
