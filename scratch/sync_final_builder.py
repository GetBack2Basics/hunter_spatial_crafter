#!/usr/bin/env python3
"""
Syncs runner/build_suitability_report.py with scratch/build_perfect_dashboard.py
"""

with open("scratch/build_perfect_dashboard.py", "r", encoding="utf-8") as f:
    perfect_code = f.read()

# Write to runner/build_suitability_report.py
with open("runner/build_suitability_report.py", "w", encoding="utf-8") as f:
    f.write(perfect_code)

print("Updated runner/build_suitability_report.py successfully.")
