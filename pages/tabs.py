# dash
import dash_bootstrap_components as dbc
from dash import html, dcc

# conexoes
import dash_cytoscape as cyto
cyto.load_extra_layouts()

# auxiliar
import components





tabs_individual = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Visão Geral", tab_id="tab-geral"),
                dbc.Tab(label="Performance de Conteúdo", tab_id="tab-conteudo"),
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
        dbc.Col([
            components.accordion_vs
        ],sm = 12)
    ]),
])

conteudo = html.Div([
    components.accordion_pc
])