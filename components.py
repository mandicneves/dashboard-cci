# dash components
import dash_bootstrap_components as dbc
from dash import html, dcc

# graficos
import plotly.graph_objects as go
from dash_bootstrap_templates import load_figure_template
import dash_cytoscape as cyto
cyto.load_extra_layouts()
tema = "cyborg"
load_figure_template(tema)


fig = go.Figure()
fig.update_layout(template = tema)

accordion = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(title="Seguidores", children=
                [
                    html.P("Seguidores por faixa etária em cada uma das plataformas"),
                    dcc.Graph(id="grafico-idade-individual", figure=fig, style={"height": "40vh", "padding": "5px", "margin-top": "10px"}),
                ] 
            ),
            dbc.AccordionItem(title="Genero", children=
                [
                    html.P("Seguidores por gênero em cada uma das plataformas"),
                    dcc.Graph(id="grafico-genero-individual", figure=fig, style={"height": "40vh", "padding": "5px", "margin-top": "10px"}),
                ] 
            ),
            dbc.AccordionItem(id="con-acord", title="Conexões", children=
                [
                    dbc.Col([
                        cyto.Cytoscape(
                            id = "grafico-conexoes-individual",
                            layout={'name': 'cola'},
                            style = {"height": "60vh"}),
                    ], sm=12, style={'align-items': 'center'})
                ] 
            ),
        ],
        flush=True,
    ),
)


