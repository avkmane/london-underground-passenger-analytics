# Executive Summary

## Objective
Transform the original London Underground statistics coursework into a reproducible analytics product combining passenger-flow engineering, statistical inference, behavioural segmentation, anomaly detection, SQL modelling, dbt transformation patterns and dashboard-ready outputs.

## Data quality
The validated run covered 268 entry records and 268 exit records across 21 hourly periods. Station sets matched with no missing values, duplicate station names or negative passenger counts. The analytical fact table contains 5,628 station-hour rows, representing 11,256 entry/exit measurements.

## Network scale
The data contains 4,672,498 entries and 4,608,120 exits, for 9,280,618 combined passenger counts. Highest network-wide combined hourly flow occurs at H08 with 999,624 entries plus exits.

## Statistical findings
Morning peak exit share averages 20.71% versus 29.87% during PM peak, a 9.16 percentage-point difference. Paired t-test: t=-7.355, p=2.35e-12; Wilcoxon: W=8,744, p=7.21e-13; Cohen's dz=0.449. AM and PM exit shares have a strong inverse relationship: Pearson r=-0.885, p=2.52e-90; Spearman rho=-0.877.

## Commuter segmentation
K-Means was evaluated for K=2 through K=6. K=2 achieved the best silhouette (0.558); K=3 retained a strong 0.490 score and was selected for operational interpretability. The three-segment model identifies 130 Residential-origin, 85 Mixed-use/interchange and 53 Employment-destination stations.

## High-volume stations
Largest combined station flows include King's Cross St. Pancras (296,198), Waterloo (296,136), Oxford Circus (258,317), Victoria (242,579), Bank & Monument (224,468), Liverpool Street (223,798) and London Bridge (220,681).

## Anomaly detection
Isolation Forest at 5% contamination flags 14 unusually shaped station-demand profiles. These are investigation candidates rather than automatic data errors.

## Limitations
The source is coursework-provided 2017 regular-weekday station data. It is aggregated at station/hour level and does not link journeys, demographics, geography or verified land-use labels. Segment labels therefore represent inferred usage patterns.
