from typing import List

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd


def plot_production(
    production_df: pd.DataFrame,
    columns2plot: List[str],
    title: str = 'Production',
) -> go._figure.Figure:
    # Create a list of traces for each column
    traces = []
    for col in columns2plot:
        traces.append(go.Scatter(x=production_df.index, y=production_df[col], name=col))

    # Create the figure
    fig = go.Figure(data=traces)

    # Update the layout
    fig.update_layout(title=title, xaxis_title='Date', yaxis_title='Power (MW)')
    
    return fig


def plot_substation_measurements(
    measurements_df: pd.DataFrame,
    station: str,
) -> go._figure.Figure:
    if station == 'B':
        prefix = 'ZLQZLQ'
    elif station == 'A':
        prefix = 'EUHIDO'
    else:
        raise ValueError(f'Invalid station {station}.')
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05)

    fig.add_trace(go.Scatter(x=measurements_df.index, y=measurements_df[f"{prefix}SPHSDL_VNUUIST"], name=f"{prefix}SPHSDL_VNUUIST"), row=1, col=1)
    fig.add_trace(go.Scatter(x=measurements_df.index, y=measurements_df[f"{prefix}SPHSDL_VNUUSOL"], name=f"{prefix}SPHSDL_VNUUSOL"), row=1, col=1)
    fig.add_trace(go.Scatter(x=measurements_df.index, y=measurements_df[f"{prefix}110KOMDROQ"], name=f"{prefix}110KOMDROQ"), row=2, col=1)

    fig.update_yaxes(title_text="Voltage in kV", row=1, col=1)
    fig.update_yaxes(title_text="Reactive Power in Mvar", row=2, col=1)
    fig.update_xaxes(title_text="Time", row=2, col=1)
    
    return fig