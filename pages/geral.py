import dash_bootstrap_components as dbc
from dash import html, dcc

from app import *
import components

layout = html.Div([
    components.tabs_geral,
])
