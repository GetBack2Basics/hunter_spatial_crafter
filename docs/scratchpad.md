# Technical Scratchpad: Wherobots Resource & Billing Optimization

## Summary of Investigation
- **Draft Invoice**: `INYXGP-DRAFT` (21 Jul – 3 Aug 2026) for GetBack2Basics (Org `ltq5l3obgb`) = US$397.03.
- **Cost Allocation**:
  - Interactive SUs (`aws-us-west-2`): $336.39 (277.84 SUs) — ~84.7%
  - Interactive SUs (`aws-ap-south-1`): $37.07 (29.07 SUs) — ~9.3%
  - Automated Batch SUs (`aws-us-west-2`): $24.13 — ~6.0%
- **Root Cause**: An interactive session was left open/running in `aws-us-west-2` during early developer setup (notebooks/MCP server) for ~278 hours.

## Key Changes Made
1. **Codebase Session Teardown**:
   - Added `try...finally: sedona.stop()` in `src/Ingestion/macquarie_spatial_ingest.py`.
   - Added `try...finally: spark.stop()` in `src/Analysis/datacenter_suitability.py`.
2. **Skill / Cheat Sheet**:
   - Updated `.agents/skills/wherobots/SKILL.md` with resource safety & cost control rules.
3. **Docs Directory Persisted Files**:
   - `docs/wherobots_credit_and_feedback_email.md`: Draft email requesting credit, sharing LinkedIn article plans, and suggesting native budget cap features.
   - `docs/linkedin_article_draft.md`: LinkedIn technical article showcasing spatial siting on Wherobots & Apache Sedona.
   - `docs/scratchpad.md`: This scratchpad file.
4. **Project Rule**:
   - Added `.agents/AGENTS.md` to ensure all future plans, scratchpads, and docs persist in `docs/`.
