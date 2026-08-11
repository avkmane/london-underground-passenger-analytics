from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio


def save_static_figures(hourly: pd.DataFrame, stations: pd.DataFrame, figure_dir: Path) -> None:
    figure_dir.mkdir(parents=True, exist_ok=True)
    network = hourly.groupby(['hour_code','hour_order'], as_index=False)[['entries','exits']].sum().sort_values('hour_order')
    fig, ax = plt.subplots(figsize=(10, 5)); ax.plot(network['hour_code'], network['entries'], marker='o', label='Entries'); ax.plot(network['hour_code'], network['exits'], marker='o', label='Exits'); ax.set_title('Network-wide hourly passenger flow'); ax.set_xlabel('Hour'); ax.set_ylabel('Passenger count'); ax.tick_params(axis='x', rotation=45); ax.legend(); fig.tight_layout(); fig.savefig(figure_dir / 'network_hourly_flow.png', dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 6))
    for segment, group in stations.groupby('segment'): ax.scatter(group['am_exit_share'], group['pm_exit_share'], alpha=0.7, label=segment)
    ax.set_title('AM vs PM exit share by station segment'); ax.set_xlabel('AM exit share'); ax.set_ylabel('PM exit share'); ax.legend(); fig.tight_layout(); fig.savefig(figure_dir / 'am_vs_pm_exit_share.png', dpi=160); plt.close(fig)
    top = stations.nlargest(15, 'total_footfall').sort_values('total_footfall'); fig, ax = plt.subplots(figsize=(9, 6)); ax.barh(top['Station'], top['total_footfall']); ax.set_title('Top 15 stations by combined footfall'); ax.set_xlabel('Entries + exits'); fig.tight_layout(); fig.savefig(figure_dir / 'top_15_stations.png', dpi=160); plt.close(fig)


def build_interactive_dashboard(hourly: pd.DataFrame, stations: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    network = hourly.groupby(['hour_code','hour_order'], as_index=False)[['entries','exits','total_flow']].sum().sort_values('hour_order')
    fig1 = go.Figure(); fig1.add_trace(go.Scatter(x=network['hour_code'], y=network['entries'], mode='lines+markers', name='Entries')); fig1.add_trace(go.Scatter(x=network['hour_code'], y=network['exits'], mode='lines+markers', name='Exits')); fig1.update_layout(title='Network-wide hourly passenger flow')
    fig2 = px.scatter(stations, x='am_exit_share', y='pm_exit_share', color='segment', size='total_footfall', hover_name='Station', title='AM vs PM exit share and commuter segment')
    fig3 = px.bar(stations.nlargest(15, 'total_footfall').sort_values('total_footfall'), x='total_footfall', y='Station', orientation='h', color='segment', title='Top 15 stations by combined footfall')
    anomalies = stations[stations['is_anomaly']].sort_values('anomaly_score'); fig4 = px.scatter(anomalies, x='employment_score', y='total_footfall', color='segment', hover_name='Station', title='Detected anomalous station patterns')
    cards = f'<h1>London Underground Passenger Analytics Dashboard</h1><p>Stations: {len(stations):,} | Combined flow: {int(stations.total_footfall.sum()):,} | Segments: {stations.segment.nunique()} | Anomalies: {int(stations.is_anomaly.sum())}</p>'
    parts = ['<html><head><meta charset="utf-8"><title>London Underground Passenger Analytics</title></head><body>', cards, pio.to_html(fig1, include_plotlyjs='cdn', full_html=False), pio.to_html(fig2, include_plotlyjs=False, full_html=False), pio.to_html(fig3, include_plotlyjs=False, full_html=False), pio.to_html(fig4, include_plotlyjs=False, full_html=False), '</body></html>']
    output_path.write_text('\n'.join(parts), encoding='utf-8')
