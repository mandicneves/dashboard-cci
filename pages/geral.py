import dash_bootstrap_components as dbc
from dash import html, dcc

from app import *
import components



layout = html.Div([




    dbc.Row([
        dbc.Col([
            dcc.Graph(id="grafico-seguidores-geral", figure=components.fig, style={"height": "30vh", "padding": "5px", "margin-top": "20px"})
        ], sm=8),
        dbc.Col([
            dcc.Graph(id="grafico-genero-geral", figure=components.fig, style={"height": "30vh", "padding": "5px", "margin-top": "20px", "margin-right": "20px"})
        ], sm=4),
    ]),







    dbc.Row([
        dbc.Col([
            dcc.Graph(id="grafico-idade-geral", figure=components.fig, style={"height": "30vh", "padding": "5px", "margin-right": "20px"})
        ], sm=12)
    ]),







    dbc.Row([
        dbc.Col([
            dcc.Graph(id="grafico-autenticos-geral", figure=components.fig, style={"height": "30vh", "padding": "5px"})
        ], sm = 5),
        dbc.Col([
            dcc.Graph(id="grafico-", figure=components.fig, style={"height": "30vh", "padding": "5px"})
        ], sm = 3),        
        dbc.Col([
            dcc.Graph(id="grafico-mapa-geral", figure=components.fig, style={"height": "30vh", "padding": "5px", "margin-right": "20px"})
        ], sm = 4),        
    ])
])









