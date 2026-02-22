# Databricks notebook source
# MAGIC %md
# MAGIC # Test Script — Simha
# MAGIC Run tests for DQM rules by loading a consumer test config and executing rules against inline test data.

# COMMAND ----------

import sys
import os

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Load consumer test config
# MAGIC Uncomment and set the path to your test config module, or use %run in Databricks:
# MAGIC `%run /Repos/<your-org>/<repo>/all_config_files_for_testing/trading_name_test_config`

# COMMAND ----------

# Load test config (defines test_data_str, config_VECCPN_Completeness, test_configurations_to_include)
import importlib.util
spec = importlib.util.spec_from_file_location(
    "trading_name_test_config",
    os.path.join(_REPO_ROOT, "all_config_files_for_testing", "trading_name_test_config.py")
)
test_config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_config)

# COMMAND ----------

# Create test table from inline CSV and run rule with test parameters
from pyspark.sql import SparkSession
from io import StringIO

spark = SparkSession.builder.getOrCreate()

# Build DataFrame from test_data_str (use None for nulls)
csv_str = test_config.test_data_str.strip()
import csv
reader = csv.DictReader(StringIO(csv_str))
rows = []
for r in reader:
    row = {}
    for k, v in r.items():
        row[k] = None if v == "None" or v == "" else v
    rows.append(row)
test_df = spark.createDataFrame(rows)
test_df.createOrReplaceTempView("test_table")

# COMMAND ----------

# Run each rule in test_configurations_to_include with config_parameters_test
from all_reusable_scripts.DQM_Global_Functions_Rule_Master import function_list_v2

for config in test_config.test_configurations_to_include:
    func_name = config["function_name"]
    params = config.get("config_parameters_test") or config.get("config_parameters_monthly_run") or {}
    mod_path = function_list_v2.get(func_name)
    if not mod_path:
        print(f"Skip (not in function_list_v2): {func_name}")
        continue
    mod = __import__(mod_path, fromlist=[func_name])
    rule_func = getattr(mod, func_name)
    sql = rule_func(**params)
    print(f"Rule: {func_name}")
    spark.sql(sql).show()

# COMMAND ----------

# MAGIC %md
# MAGIC Compare expected vs actual row-level outcomes here (e.g. from test data with Expected Outcome column).
