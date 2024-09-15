import dash_bootstrap_components as dbc
from dash import html, dcc

from pages import tabs

import plotly.graph_objects as go

layout = html.Div([
    dbc.Row([
        tabs.tabs
    ])
])


