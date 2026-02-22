# DQM Framework — Data Quality Measurement Platform

A reusable, parameterised Data Quality Measurement (DQM) framework designed to run on **Databricks**. It runs many rules for many consumers on a schedule and stores all results in a central **Results Catalog** (Delta table).

## What This Repo Contains

| Folder / File | Purpose |
|---------------|--------|
| **all_rules_repository/** | Rule logic: one Python module per rule (function returns SQL string). |
| **all_config_files/** | Consumer configs: which rules run for which consumer and with what parameters. |
| **all_config_files_for_testing/** | Test configs and inline CSV test data for rule validation. |
| **all_reusable_scripts/** | `DQM_Global_Functions_Rule_Master.py` (rule registry) and `Universal_Execution_Script.py` (orchestration). |
| **development_notebooks/** | Sandbox for building and testing new rules before promoting. |
| **Test_Notebooks/** | Scripts that run tests by loading test configs. |
| **scripts/** | Utility scripts (e.g. create Results Catalog table in Databricks). |

## Quick Start

**In Databricks:** Add this repo in **Repos** (after pushing from here to GitHub). The framework runs in Databricks by cloning from GitHub; you develop and push from this environment.

1. **Clone this repo** into your Databricks workspace (Repos) or locally.
2. **Create the Results Catalog** in Databricks: run the SQL in `scripts/create_results_catalog.sql`.
3. **Link repo in Databricks** (Repos → Add Repo) and set branch to `main`.
4. **Create a per-consumer Job** in Databricks Workflows: run `all_reusable_scripts/Universal_Execution_Script.py` with parameter `consumer_name` (e.g. `Trading Name`). Use a **job cluster** and set **Git** to this repo, branch **main**; then set the task's notebook source to **Git**.
5. **Create a Master Job** (type: Run Job) that runs the per-consumer job(s) on a schedule (e.g. monthly).

## Branching

- **main** — Production; Databricks jobs run from here.
- **development** — Integration branch (optional).
- **feature/*** — Develop new rules; merge to development then main.

## Requirements

- Databricks workspace (Repos, Workflows, Spark)
- GitHub (this repo)
- Python 3.x / PySpark (for running rules)

## Push to GitHub from this environment (secure)

The repo is ready to push. To avoid credential prompts and push **securely from Cursor/this environment**:

1. **One-time setup** — See **[docs/SETUP_GITHUB_PUSH.md](docs/SETUP_GITHUB_PUSH.md)**. You can use:
   - **Git + macOS Keychain**: `git config --global credential.helper osxkeychain`, then one `git push` (enter PAT when prompted); after that, pushes work without prompts.
   - **GitHub CLI**: `gh auth login`, then push.
   - **SSH**: Add your SSH key to GitHub and set `origin` to `git@github.com:USER/repo.git`.
2. **Set your remote** (if different from `simha/dqm-framework`):
   ```bash
   git remote set-url origin https://github.com/YOUR_USERNAME/dqm-framework.git
   ```
3. **Push** (after one-time credential setup, this works without typing credentials):
   ```bash
   git push -u origin main
   ```
   Or run: `./scripts/push_to_github.sh`

Credentials are stored by the system (Keychain, `gh`, or SSH), not in the repo.

## Documentation

- **DQM_FRAMEWORK_UNDERSTANDING.md** (in parent folder) — Full framework spec.
- **DQM_Build_Approach_Guide.md** (in parent folder) — Step-by-step build guide for beginners.
