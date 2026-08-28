#!/usr/bin/env python3
content = open('runner/build_suitability_report.py', encoding='utf-8').read()
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if 'speed-mechanics' in line or 'simulation-sandbox' in line or '.container {' in line:
        print(f'Line {i}: {line[:140]}')
