# Project Rules & Guidance

## Documentation, Plans & Scratchpad Persistence Rule

- **Documentation & Artifact Location**: All implementation plans, technical scratchpads, email drafts, articles, and research notes generated during tasks MUST be persisted in the repository's [`docs/`](file:///c:/Projects/hunter_spatial_crafter/docs) directory.
- **Naming Conventions**: Use clear descriptive filenames in `docs/` (e.g., `docs/implementation_plan.md`, `docs/scratchpad.md`, `docs/linkedin_article_draft.md`, `docs/wherobots_credit_and_feedback_email.md`).

## Compute Resource Teardown & Cost Protection Rule

- **Mandatory Instance & Session Teardown**: Always ensure that all compute instances, interactive Wherobots runtimes, Sedona/SparkContext sessions (`spark.stop()`), and background execution tasks are explicitly terminated immediately after execution to prevent billing blowouts.
- **Reporting Obligation**: In every final response after executing computational jobs, explicitly check and report the compute/instance shutdown status to the user.
