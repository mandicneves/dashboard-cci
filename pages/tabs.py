import dash_bootstrap_components as dbc
from dash import html, dcc

import dash_cytoscape as cyto
cyto.load_extra_layouts()

import components


tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Visão Geral", tab_id="tab-geral"),
                dbc.Tab(label="Métricas Análise", tab_id="tab-metricas"),
                dbc.Tab(label="Conteúdo", tab_id="tab-conteudo"),
            ],
            id="tabs",
            active_tab="tab-geral",
            style={"padding": "10px", "margin": "10px"}
        ),
        html.Div(id="content"),
    ]
)

visao_geral = html.Div([
    dbc.Row([
        dbc.Col([]),
        dbc.Col([
            html.H4("Rede de conexões", style={"display": "flex", "justify-content": "center", "margin-top": "15px"}),
            cyto.Cytoscape(
                id = "grafico-conexoes-individual",
                layout={'name': 'cola'},
                style = {"height": "80vh"}
            )
        ], sm=5),
    ]),
    
    
    
    
    
])

metricas_analise = html.Div([
])

conteudo = dbc.Row([
    dbc.Row([dbc.Col([
        dcc.Graph(id="grafico-total-posts", figure=components.fig, style={"height": "28vh", "padding": "10px"})
    ])]),
    dbc.Row([dbc.Col([
        dcc.Graph(id="grafico-total-posts", figure=components.fig, style={"height": "28vh", "padding": "10px"})
    ])]),
    dbc.Row([dbc.Col([
        dcc.Graph(id="grafico-total-posts", figure=components.fig, style={"height": "28vh", "padding": "10px"})
    ])]),
])