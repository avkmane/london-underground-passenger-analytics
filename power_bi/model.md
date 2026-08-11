# Power BI semantic-model handoff

The pipeline produces two Power BI-ready tables when authorised raw data is present:

- `data/processed/hourly_station_flow.csv`: grain = one station × one hour (5,628 rows).
- `data/processed/station_metrics.csv`: grain = one station (268 rows), including commuter segment and anomaly flags.

Recommended model:
1. Load hourly flow as `FactHourlyFlow`.
2. Load station metrics as `DimStationMetrics`.
3. Create one-to-many relationship from `DimStationMetrics[Station]` to `FactHourlyFlow[Station]`.
4. Sort `FactHourlyFlow[hour_code]` by `FactHourlyFlow[hour_order]`.

Recommended report pages: Executive Overview; Hourly Demand; Peak Flow & Net Arrivals; Commuter Segments; Station Drill-through; Anomalies & Data Quality.

A binary `.pbix` is not claimed because Power BI Desktop was not available in the execution environment.
