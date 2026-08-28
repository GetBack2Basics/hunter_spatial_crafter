#!/usr/bin/env python3
import subprocess
import sys

result = subprocess.run(
    ["git", "show", "3a9aef2:runner/build_suitability_report.py"],
    capture_output=True, text=True, encoding="utf-8", errors="replace",
    cwd="c:/Projects/hunter_spatial_crafter"
)
content = result.stdout

idx = content.find('id="speed-mechanics"')
if idx == -1:
    print("NOT FOUND in 3a9aef2")
    import re
    tabs = re.findall(r"switchTab\(event,\s*['\"]([^'\"]+)['\"]", content)
    print("Tabs:", tabs)
else:
    end = content.find('<!-- Tab', idx + 10)
    if end == -1:
        end = idx + 5000
    print(content[idx:end])
