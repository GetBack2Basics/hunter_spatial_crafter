import os
from wherobots import WherobotsJob

API_KEY = "wbk_user_0ccdpe9bdefvydj9vlj5mf4gx1vi7nbbm03lk4ntes8kebqe6okm78edmc50b9vo"

def main():
    print("Initializing Wherobots Job submission...")
    
    # Declare dependencies
    config_dep = WherobotsJob.add_file_dependency("config/macquarie.json")
    
    # Initialize job
    job = WherobotsJob(
        script="src/Ingestion/macquarie_spatial_ingest.py",
        name="macquarie-spatial-etl",
        runtime="tiny",
        api_key=API_KEY,
        dependencies=[config_dep],
    )
    
    # Submit job
    print("Submitting job to Wherobots...")
    job.submit()
    print(f"Job submitted successfully. Run ID: {job.run_id}")
    
    # Wait for completion and stream logs
    print("Waiting for job completion...")
    status = job.wait_for_completion(stream_logs=True)
    print(f"Job finished with status: {status}")

if __name__ == "__main__":
    main()
