"""
DQM Global Function File — Rule registry.
Maps each rule identifier (function name) to the Python module path that contains the rule function.
Update this file when you add a new rule. Incorrect paths will break the framework.
"""

# Map: function_name (str) -> Python module path (str) for importlib.import_module
# Module must define a function with the same name as the key.
function_list_v2 = {
    "Rule_VECCPN_Completeness": "all_rules_repository.TradingName.Rule_VECCPN_Completeness",
    # Add more rules as you build them, e.g.:
    # "Rule_CHZZJ9_Completeness": "all_rules_repository.TradingName.Rule_CHZZJ9_Completeness",
}
