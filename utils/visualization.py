from typing import List

import plotly.graph_objs as go
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