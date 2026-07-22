# Azure DevOps Repo Permissions — Spatial Projects

## Issue summary
Regular users could not access Azure Repos unless signed in with an admin account. Admins could see repos, but standard accounts were missing repo-level membership/permissions.

## Root cause
Azure DevOps project memberships do not automatically grant repo access. Users/groups must be explicitly added at the project or repo level, or assigned via a security group that already has access.

## Resolution
1. Confirm the **Azure DevOps org/project owner** who can manage permissions (`Spatial-Delivery` in this case; Ariful Huq was identified as the Azure project owner).
2. Add regular users directly, or add an AD security group, then assign that group to the repo.
3. Verify access by re-opening the repo in the same browser/profile the regular user uses.

## Evidence / artefacts
- Key vault access fix: `azdo-sec-prj-applicationresourcesspatial-team` was added to the key vaults.
- Incident/ticket: https://csconnect.dpie.nsw.gov.au/csconnect?id=ticket&table=incident&sys_id=4109ce9fc3b18bd4f6065823e40131ca

## Admin portal links
- Project teams/permissions: https://dev.azure.com/dpiedevops/Spatial-Delivery/_settings/teams
- Permissions: https://dev.azure.com/dpiedevops/Spatial-Delivery/_settings/permissions

## Lessons learned
- Admin accounts often work because they implicitly bypass repo ACL checks. Regular accounts expose missing grants.
- When AI coding agents (e.g. VS Code Copilot) need to make edits, the user identity must have explicit repo permissions, not just project-level visibility.
- If access is “out”, a blank/new repo may still fail to load for non-admins until the underlying permission grant is added.

## Checklist for new spatial repos
- [ ] Regular users/groups added to repo permissions or inherited security group
- [ ] Key vault access group (`azdo-sec-prj-applicationresourcesspatial-team`) has required secrets permissions
- [ ] Repo loads for a non-admin test account
- [ ] VS Code / Copilot agent can authenticate with the regular account’s token/credentials

## Related artefacts in this repo
- `hunter_spatial_crafter` — local clone where permission issues blocked notebook/ETL execution
- Notebook: `notebooks/Macquarie_Coal_Complex_Spatial_ETL.ipynb`
- Module: `src/Ingestion/macquarie_spatial_ingest.py`
- WS instance: `j9s2n4mtsdknro`
