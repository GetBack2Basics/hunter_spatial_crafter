import os

playbook_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "CheatSheets", "wherobots_antigravity_playbook.md"))

with open(playbook_path, "r", encoding="utf-8") as f:
    text = f.read()

# Clean any existing duplicated addition if present
split_marker = "## Incremental Spatial Compute & Cost Optimization Principles"
if split_marker in text:
    # Reset to base by reading from git
    pass

new_section = """
---

## Incremental Spatial Compute & Cost Optimization Principles

When designing large-scale spatial ETL and multi-criteria decision analysis (MCDA) pipelines on Wherobots Cloud, managing cloud compute spend and execution latency requires adhering to four core engineering optimization patterns:

```mermaid
graph TD
    A[Raw Spatial Portals / Cadastre] -->|Data Fingerprinting & ETag Validation| B(Unchanged: Read Havasu Cache)
    A -->|Changed / New Features| C[Target Ingestion & Reprojection]
    C -->|Materialized Intermediate Tables| D[Topological Buffers & Net Developable Overlays]
    D -->|Distance Matrices| E[Downstream Vector Scoring Matrix]
    E -->|JSON Payload Export| F[In-Browser Client Execution: DuckDB-WASM & JS]
```

### 1. Decoupling Heavy Geometry Calculations from Lightweight Scoring
- **The Problem**: Spatial pipelines typically involve heavy geometric operations (reprojecting to metric CRS like `EPSG:7856`, repairing topology via `ST_MakeValid`, applying 30m/20m buffers, and computing `ST_Difference` masks across millions of polygons) and lightweight mathematical scoring (sigmoidal acoustic decay, distance decay, and weight normalization).
- **The Best Practice**: Materialize intermediate spatial distance matrices and developable area boundaries into permanent Havasu/GeoParquet tables. When adjusting MCDA weighting criteria (e.g. altering power proximity from 40% to 50%) or modifying sigmoidal curve steepness ($k$), **never re-execute the multi-million polygon spatial joins**. Only re-evaluate the downstream scoring matrix or delegate it 100% to client-side compute.

### 2. Source-Level Data Fingerprinting & Snapshot Memoization
- **The Problem**: Public cadastre (15.4M lots), national rail networks (275k features), and transmission grids (241k features) update infrequently. Re-ingesting full datasets on every run consumes unnecessary cluster hours.
- **The Best Practice**: Hash upstream dataset metadata (ETags, GeoParquet file hashes, Iceberg snapshot manifest IDs). The ingestion step checks the hash; if unchanged, it skips ingestion and reads directly from the existing Havasu catalog.

### 3. Delta Partition Processing (Iceberg Time-Travel)
- **The Problem**: When quarterly cadastral or infrastructure updates are released, re-running full spatial joins over the entire continent is computationally redundant.
- **The Best Practice**: Leverage Apache Iceberg snapshot metadata to isolate and process only modified or appended geometries (`ST_Changes`) rather than scanning untouched partitions.

### 4. Zero-Cost Client Compute Offloading (DuckDB-WASM & JS)
- **The Problem**: Supporting interactive public What-If sandboxes via server-side spatial SQL calls incurs continuous cloud infrastructure costs per user interaction.
- **The Best Practice**: Precompute heavy topological winding distances and area buffers once on Wherobots Cloud. Embed the precomputed matrix in a static HTML report and use client-side JavaScript or **DuckDB-WASM** (via [GeoLibre](https://github.com/opengeos/GeoLibre)) to execute instant (<1ms) multi-criteria recalculations directly in the user browser at **$0.00 cloud compute cost**.
"""

anti_patterns = """
### Anti-pattern 11: Re-running heavy spatial buffers and joins during parameter tuning
- **Why this fails**: Re-executing `ST_Buffer` and `ST_Union_Aggr` over millions of polygons just to change a 40% weight to 50% or tweak a sigmoidal threshold costs unnecessary cloud compute and delays iteration.
- **Better approach**: Materialize topological distance matrices and net buildable pad areas into intermediate GeoParquet / Havasu tables; evaluate scoring functions downstream or client-side.

### Anti-pattern 12: Ingesting static continental cadastral and infrastructure layers on every run
- **Why this fails**: Re-fetching 15M+ cadastral lots or 275k rail vectors on every pipeline run wastes bandwidth and Spark compute.
- **Better approach**: Compute cryptographic ETags / content hashes and only ingest deltas using Iceberg snapshots.
"""

# Let's restore from git HEAD first
import subprocess
subprocess.run(["git", "-C", os.path.dirname(playbook_path), "checkout", "wherobots_antigravity_playbook.md"], check=True)

with open(playbook_path, "r", encoding="utf-8") as f:
    orig = f.read()

# Insert before '## What this gives you'
target = "## What this gives you"
updated = orig.replace(target, new_section + "\n" + target) + "\n" + anti_patterns

with open(playbook_path, "w", encoding="utf-8") as f:
    f.write(updated)

print("Playbook rewritten cleanly.")
