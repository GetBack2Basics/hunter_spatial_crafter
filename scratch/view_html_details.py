with open("runner/national_suitability_report.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(410, 450):
    if i < len(lines):
        print(f"{i+1}: {lines[i].strip()}")
