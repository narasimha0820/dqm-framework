# Development notebooks — Simha

Use this folder to build and try new rules before promoting them to `all_rules_repository`.

1. Implement the rule function (e.g. `Rule_<ID>_<Dimension>`) and config in a notebook here.
2. Dry-run: render SQL and run `spark.sql(sql).show()`.
3. When ready, copy the rule to `all_rules_repository/...` and config to `all_config_files/...`, and update `DQM_Global_Functions_Rule_Master.py`.
