# Resume-ready project entry

## London Underground Passenger Flow Analytics & Station Segmentation
**Python | SQL | Pandas | NumPy | SciPy | scikit-learn | dbt | SQLite/DuckDB | Plotly | Power BI-ready DAX | pytest | GitHub Actions | Docker**

- Engineered an end-to-end passenger-flow analytics pipeline across **268 London Underground stations, 21 hourly periods and 11,256 entry/exit measurements**, transforming **9.28M combined entry/exit counts** into validated station-hour and station-level analytical marts using Python, Pandas and SQL.
- Replaced heuristic peak interpretation with statistical evidence by identifying a **strong inverse AM-vs-PM exit-share relationship (Pearson r = -0.885, p < 1e-89)** and a **9.16 percentage-point higher mean PM exit share**, validated through paired t-test, Wilcoxon test and effect-size analysis.
- Segmented **268 stations into 130 residential-origin, 85 mixed-use/interchange and 53 employment-destination profiles** using standardised K-Means features (**silhouette = 0.490**), then flagged **14 atypical demand patterns** with Isolation Forest for targeted investigation.
- Productionised the analysis into modular Python packages, SQL views, a dbt staging/intermediate/mart design, Power BI-ready semantic design, Plotly visualisation layer, **5/5 locally passing pytest checks**, GitHub Actions CI and Docker packaging.

## Short two-bullet CV version

- Built an end-to-end **Python/SQL passenger analytics platform** across **268 London Underground stations and 11,256 hourly entry/exit measurements**, processing **9.28M combined counts** into tested analytical marts and quantifying a **-0.885 AM/PM peak correlation** through statistical inference.
- Developed K-Means commuter segmentation (**silhouette 0.490**) identifying **130 residential, 85 mixed/interchange and 53 employment-destination stations**, added Isolation Forest anomaly detection for **14 unusual profiles**, and productionised the solution with dbt modelling, Plotly, Power BI-ready DAX/semantic design, pytest, GitHub Actions and Docker packaging.
