"""
Consumer config: Trading Name.
Defines which rules run for this consumer and their parameters for the monthly run.
"""

# Rule config for VECCPN Completeness (production / monthly run parameters)
config_VECCPN_Completeness = {
    "function_name": "Rule_VECCPN_Completeness",
    "config_parameters_monthly_run": {
        "rule_id": "VECCPN",
        "extract_date": "extract_date",
        "end_at": "end_at",
        "table_name": "enterprise.my_schema.my_trading_table",  # Replace with your catalog.schema.table
        "main_field": "trading_name",
        "filter_field": "customer_type",
        "filter_value": "'CORP','TRA'",
        "parameter_for_start_dt": -1,
        "parameter_for_end_dt": 0,
    },
    "config_parameters_test": {
        "rule_id": "VECCPN",
        "extract_date": "extract_date",
        "end_at": "end_at",
        "table_name": "test_table",
        "main_field": "main_field",
        "filter_field": "filter_field",
        "filter_value": "'TRA'",
        "parameter_for_start_dt": 1,
        "parameter_for_end_dt": 1,
    },
    "test_file": "test_data_csv",
    "test_table": "test_data_str",
}

# Consolidation: list of rule configs for this consumer (used by Universal_Execution_Script)
final_config = [config_VECCPN_Completeness]
