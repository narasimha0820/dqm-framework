# Databricks notebook source
# MAGIC %md
# MAGIC # Universal Execution Script
# MAGIC Runs all DQM rules for a given consumer and writes results to the Results Catalog.
# MAGIC **Job parameter:** `consumer_name` (e.g. "Trading Name")

# COMMAND ----------

import sys
import os
import importlib
from datetime import date
from pyspark.sql import SparkSession

# Repo root (when run from Repos: .../dqm-framework/all_reusable_scripts/Universal_Execution_Script.py)
try:
    _script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _script_dir = os.getcwd()
_REPO_ROOT = os.path.abspath(os.path.join(_script_dir, ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

# COMMAND ----------

def get_consumer_name():
    """Get consumer_name from Databricks widget or environment."""
    try:
        return str(dbutils.widgets.get("consumer_name")).strip()
    except Exception:
        pass
    return os.environ.get("DQM_CONSUMER_NAME", "Trading Name")

# COMMAND ----------

# Map consumer_name (job parameter) to config module path
CONSUMER_CONFIG_MAP = {
    "Trading Name": "all_config_files.trading_name_config",
    # Add more consumers, e.g. "Finance": "all_config_files.finance_config",
}

# COMMAND ----------

def load_final_config(consumer_name):
    """Load final_config list for the given consumer."""
    module_path = CONSUMER_CONFIG_MAP.get(consumer_name)
    if not module_path:
        raise ValueError(f"Unknown consumer_name: {consumer_name}. Known: {list(CONSUMER_CONFIG_MAP.keys())}")
    mod = importlib.import_module(module_path)
    return mod.final_config

# COMMAND ----------

def get_rule_function(function_name):
    """Resolve rule function from DQM_Global_Functions_Rule_Master.function_list_v2."""
    from all_reusable_scripts.DQM_Global_Functions_Rule_Master import function_list_v2
    module_path = function_list_v2.get(function_name)
    if not module_path:
        raise ValueError(f"Rule not registered: {function_name}. Check DQM_Global_Functions_Rule_Master.py")
    mod = importlib.import_module(module_path)
    return getattr(mod, function_name)

# COMMAND ----------

def compute_rule_execution_status(row):
    """Set S/F/Q based on counts (quarantine conditions)."""
    assessed = row.get("total_records_assessed") or 0
    passed = row.get("total_records_passed") or 0
    failed = row.get("total_records_failed") or 0
    na = row.get("total_records_not_applicable") or 0
    if assessed == 0 or assessed == na or (passed == 0 and failed == 0):
        return "Q"  # Quarantine
    return "S" if failed == 0 else "F"

# COMMAND ----------

def run_consumer(consumer_name, results_catalog_schema="enterprise_dqm_results", results_table="rule_results"):
    """Run all rules for the consumer and write to Results Catalog."""
    spark = SparkSession.builder.getOrCreate()
    final_config = load_final_config(consumer_name)
    rule_executed_in = os.environ.get("DQM_RULE_EXECUTED_IN", "Databricks")
    rows = []

    for config in final_config:
        function_name = config["function_name"]
        params = config.get("config_parameters_monthly_run") or config.get("config_parameters_test") or {}
        try:
            rule_func = get_rule_function(function_name)
            sql = rule_func(**params)
            df = spark.sql(sql)
            row = df.collect()[0].asDict()
        except Exception as e:
            row = {
                "rule_unique_id": params.get("rule_id", "?"),
                "run_date": date.today(),
                "extract_date_range_start": None,
                "extract_date_range_end": None,
                "total_records_assessed": 0,
                "total_records_passed": 0,
                "total_records_failed": 0,
                "total_records_not_applicable": 0,
            }
            row["rule_execution_status"] = "F"
            raise RuntimeError(f"Rule {function_name} failed") from e

        row["rule_executed_in"] = rule_executed_in
        row["rule_execution_status"] = compute_rule_execution_status(row)
        row["consumer_name"] = consumer_name
        rows.append(row)

    if not rows:
        return

    # Write to Results Catalog
    result_df = spark.createDataFrame(rows)
    full_table = f"{results_catalog_schema}.{results_table}"
    result_df.write.format("delta").mode("append").saveAsTable(full_table)
    print(f"Wrote {len(rows)} row(s) to {full_table}")

# COMMAND ----------

if __name__ == "__main__" or "dbutils" in dir():
    consumer_name = get_consumer_name()
    run_consumer(consumer_name)
