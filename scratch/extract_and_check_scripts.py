import re
import subprocess
import os

with open("runner/national_suitability_report.html", "r", encoding="utf-8") as f:
    html = f.read()

scripts = re.findall(r"<script(?:\s+[^>]*)?>(.*?)</script>", html, flags=re.DOTALL)
print(f"Found {len(scripts)} script blocks in runner/national_suitability_report.html")

for idx, script in enumerate(scripts, 1):
    js_filename = f"scratch/test_script_{idx}.js"
    with open(js_filename, "w", encoding="utf-8") as jf:
        jf.write(script)
    
    # Run node syntax check
    res = subprocess.run(["node", "--check", js_filename], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"ERROR in script block #{idx} ({js_filename}):")
        print(res.stderr)
    else:
        print(f"Script block #{idx} ({js_filename}) syntax is VALID! (Length: {len(script)} bytes)")
