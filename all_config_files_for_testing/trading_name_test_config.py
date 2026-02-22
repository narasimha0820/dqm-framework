"""
Test config for consumer: Trading Name.
Use inline CSV test data; table_name in config points to test_table (temp view).
"""

# Inline CSV test data. Use None for nulls (except literal strings 'NULL' or "").
test_data_str = """
main_field,filter_field,extract_date,end_at
Arun Munshi,NULL,2024-06-05,None
Dom M,None,2024-06-05,None
James C,TRA,2024-06-05,None
Harini J,YPC,2024-06-05,None
None,TRA,2024-06-05,None
NULL,TRA,2024-06-05,None
,TRA,2024-06-05,None
Arun Munshi,TRA,2024-06-05,None
Dom M,TRA,2024-06-05,None
"""

# Same rule config with test parameters (table_name -> test_table)
config_VECCPN_Completeness = {
    "function_name": "Rule_VECCPN_Completeness",
    "config_parameters_monthly_run": {
        "rule_id": "VECCPN",
        "extract_date": "extract_date",
        "end_at": "end_at",
        "table_name": "enterprise.my_schema.my_trading_table",
        "main_field": "trading_name",
        "filter_field": "customer_type",
        "filter_value": "'TRA'",
        "parameter_for_start_dt": 1,
        "parameter_for_end_dt": 1,
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

# Which tests to run in this notebook
test_configurations_to_include = [config_VECCPN_Completeness]
