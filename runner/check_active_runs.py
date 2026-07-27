import sys
from wherobots import WherobotsJob

API_KEY = "wbk_user_0ccdpe9bdefvydj9vlj5mf4gx1vi7nbbm03lk4ntes8kebqe6okm78edmc50b9vo"

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("Checking active runs on Wherobots...")
    try:
        runs = WherobotsJob.list_runs(api_key=API_KEY, size=5)
        print("\n=== Recent Wherobots Job Runs ===")
        for run in runs.items:
            print(f"ID: {run.id} | Name: {run.name} | Status: {run.status.value} | Created: {run.created_at if hasattr(run, 'created_at') else 'N/A'}")
    except Exception as e:
        print("Error fetching runs:", e)

if __name__ == "__main__":
    main()
