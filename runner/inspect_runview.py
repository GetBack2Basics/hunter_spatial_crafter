import sys
from wherobots import WherobotsJob

API_KEY = "wbk_user_0ccdpe9bdefvydj9vlj5mf4gx1vi7nbbm03lk4ntes8kebqe6okm78edmc50b9vo"

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    runs = WherobotsJob.list_runs(api_key=API_KEY, size=1)
    if runs.items:
        r = runs.items[0]
        print("RunView class:", type(r))
        print("Attributes:", dir(r))
        try:
            print("Dict representation:", r.__dict__)
        except:
            pass

if __name__ == "__main__":
    main()
