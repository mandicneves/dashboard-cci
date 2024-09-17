import dash_bootstrap_components as dbc
from dash import html, dcc

from app import *
import components



layout = html.Div([





    # primeira linha
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="grafico-seguidores-geral", figure=components.fig, style={"height": "30vh", "padding": "5px", "margin-top": "20px"})
        ], sm=8),
        dbc.Col([
            dcc.Graph(id="grafico-genero-geral", figure=components.fig, style={"height": "30vh", "padding": "5px", "margin-top": "20px", "margin-right": "20px"})
        ], sm=4),
    ], className="g-0"),


    # segunda linha
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="grafico-idade-geral", figure=components.fig, style={"height": "30vh", "padding": "5px", "margin-right": "20px"})
        ], sm=12)
    ]),



    # terceira linha
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="grafico-autenticos-geral", figure=components.fig, style={"height": "30vh", "padding": "5px"})
        ], sm = 6),       
        dbc.Col([
            dcc.Graph(id="grafico-mapa-geral", figure=components.fig, style={"height": "30vh", "padding": "5px", "margin-right": "20px"})
        ], sm = 6),        
    ], className="g-0")
])
