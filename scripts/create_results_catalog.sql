-- Run this in Databricks SQL or a Databricks notebook to create the Results Catalog.
-- Adjust catalog/schema names if you use Unity Catalog (e.g. your_catalog instead of default).

CREATE SCHEMA IF NOT EXISTS enterprise_dqm_results;

CREATE TABLE IF NOT EXISTS enterprise_dqm_results.rule_results (
  rule_executed_in             STRING   COMMENT 'Where the rule ran e.g. Databricks',
  rule_unique_id               STRING   COMMENT '6-char rule ID e.g. VECCPN',
  run_date                     DATE     COMMENT 'Date of run',
  extract_date_range_start     DATE     COMMENT 'Min extract_date from data',
  extract_date_range_end       DATE     COMMENT 'Max extract_date from data',
  total_records_assessed       BIGINT,
  total_records_passed         BIGINT,
  total_records_failed         BIGINT,
  total_records_not_applicable BIGINT,
  rule_execution_status        STRING   COMMENT 'S=Success, F=Failure, Q=Quarantine',
  consumer_name                STRING   COMMENT 'Which consumer this run was for'
)
USING DELTA
COMMENT 'Unified DQM results — one row per rule execution';

-- Quarantine: set rule_execution_status = 'Q' when
--   total_records_assessed = 0 OR
--   total_records_assessed = total_records_not_applicable OR
--   (total_records_passed = 0 AND total_records_failed = 0)
