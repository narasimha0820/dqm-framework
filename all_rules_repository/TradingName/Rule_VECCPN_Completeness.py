"""
Rule VECCPN — Completeness.
Checks that a main field is not blank or null when a filter condition is met.
"""


def Rule_VECCPN_Completeness(
    rule_id,
    extract_date,
    end_at,
    table_name,
    main_field,
    filter_field,
    filter_value,
    parameter_for_start_dt,
    parameter_for_end_dt,
):
    """
    Returns a SQL string that evaluates completeness per row and aggregates to one row.
    ROW_STATUS: PASS (has value), FAIL (null/blank), NOT_APPLICABLE (filter not met).
    """
    return f"""
    SELECT
      '{rule_id}' AS rule_unique_id,
      current_date() AS run_date,
      MIN({extract_date}) AS extract_date_range_start,
      MAX({extract_date}) AS extract_date_range_end,
      COUNT(*) AS total_records_assessed,
      SUM(CASE WHEN ROW_STATUS = 'PASS' THEN 1 ELSE 0 END) AS total_records_passed,
      SUM(CASE WHEN ROW_STATUS = 'FAIL' THEN 1 ELSE 0 END) AS total_records_failed,
      SUM(CASE WHEN ROW_STATUS = 'NOT_APPLICABLE' THEN 1 ELSE 0 END) AS total_records_not_applicable
    FROM (
      SELECT
        *,
        CASE
          WHEN UPPER(TRIM(COALESCE(CAST({filter_field} AS STRING), ''))) NOT IN ({filter_value})
               OR {filter_field} IS NULL
               OR TRIM(COALESCE(CAST({filter_field} AS STRING), '')) = ''
               OR UPPER(TRIM(CAST({filter_field} AS STRING))) = 'NULL'
            THEN 'NOT_APPLICABLE'
          WHEN {main_field} IS NULL
               OR TRIM(COALESCE(CAST({main_field} AS STRING), '')) = ''
               OR UPPER(TRIM(CAST({main_field} AS STRING))) = 'NULL'
            THEN 'FAIL'
          ELSE 'PASS'
        END AS ROW_STATUS
      FROM {table_name}
      WHERE 1=1
        AND ({end_at}) IS NULL
    ) t
    """
