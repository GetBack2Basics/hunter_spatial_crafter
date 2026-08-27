# Project Rules & Guidance

## Documentation, Plans & Scratchpad Persistence Rule

- **Documentation & Artifact Location**: All implementation plans, technical scratchpads, email drafts, articles, and research notes generated during tasks MUST be persisted in the repository's [`docs/`](file:///c:/Projects/hunter_spatial_crafter/docs) directory.
- **Naming Conventions**: Use clear descriptive filenames in `docs/` (e.g., `docs/implementation_plan.md`, `docs/scratchpad.md`, `docs/linkedin_article_draft.md`, `docs/wherobots_credit_and_feedback_email.md`).

## Compute Resource Teardown & Cost Protection Rule

- **Mandatory Instance & Session Teardown**: Always ensure that all compute instances, interactive Wherobots runtimes, Sedona/SparkContext sessions (`spark.stop()`), and background execution tasks are explicitly terminated immediately after execution to prevent billing blowouts.
- **Reporting Obligation**: In every final response after executing computational jobs, explicitly check and report the compute/instance shutdown status to the user.

## Incremental Spatial Compute & Cost Optimization Memory

- **Engineering Playbook Reference**: All spatial ETL pipelines must follow the [Wherobots & Antigravity Engineering Playbook](https://github.com/GetBack2Basics/CheatSheets/blob/main/wherobots_antigravity_playbook.md).
- **Decoupled Geometry vs. Scoring**: Separate heavy geometric calculations (CRS transforms, topological buffers, `ST_Difference` masks) from lightweight mathematical scoring ($S_{\text{power}}$, $S_{\text{sensitive}}$, $S_{\text{water}}$). Changing weights or sigmoidal curve parameters must never re-trigger heavy spatial joins.
- **Data Fingerprinting & Memoization**: Use cryptographic hashing (ETags, GeoParquet file hashes, Iceberg snapshot IDs) to skip re-running untouched spatial layers.
- **Delta Partition Processing**: Use Apache Iceberg time-travel / partition manifests to process only newly altered geometries (`ST_Changes`).
- **Zero-Cost Client Offloading**: Offload interactive What-If scenario modeling, sensitivity tests, and slider re-scoring 100% to client-side DuckDB-WASM and JavaScript ($0.00 cloud compute cost).
