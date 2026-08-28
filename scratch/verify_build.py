#!/usr/bin/env python3
import re

with open("runner/national_suitability_report.html", "r", encoding="utf-8") as f:
    content = f.read()

print("is_simulated occurrences:", len(re.findall(r'"is_simulated"', content)))
print("MICRO-SITED occurrences:", len(re.findall(r"MICRO-SITED", content)))
print("SIMULATED BASELINE occurrences:", len(re.findall(r"SIMULATED BASELINE", content)))
print("crossorigin occurrences:", len(re.findall(r"crossorigin", content)))
print("integrity= occurrences:", len(re.findall(r"integrity=", content)))
print("isMicroSited occurrences:", len(re.findall(r"isMicroSited", content)))
print("INYXGP occurrences:", len(re.findall(r"INYXGP", content)))
print("provenanceBadge occurrences:", len(re.findall(r"provenanceBadge", content)))
print("simulatedGroupTag occurrences:", len(re.findall(r"simulatedGroupTag", content)))
