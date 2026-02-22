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

## Push to your GitHub

The repo is initialized with branch `main` and a first commit. To push to **your** GitHub:

1. **Create a new repository** on GitHub (e.g. `dqm-framework`) — do not add a README or .gitignore so the repo is empty.
2. **Set your remote** (replace `YOUR_USERNAME` and repo name if different):
   ```bash
   cd /path/to/dqm-framework
   git remote set-url origin https://github.com/YOUR_USERNAME/dqm-framework.git
   # Or use SSH: git remote set-url origin git@github.com:YOUR_USERNAME/dqm-framework.git
   ```
3. **Push:**
   ```bash
   git push -u origin main
   ```
   Use a Personal Access Token (PAT) if prompted for password, or ensure SSH keys are set up for SSH URLs.

## Documentation

- **DQM_FRAMEWORK_UNDERSTANDING.md** (in parent folder) — Full framework spec.
- **DQM_Build_Approach_Guide.md** (in parent folder) — Step-by-step build guide for beginners.
