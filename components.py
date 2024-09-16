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

# componentes
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
            dbc.AccordionItem(
                item_id="conexao-accordion", title="Conexões", children=
                [
                    dbc.Col([
                        html.Div([], id="grafico-conexoes-individual")
                    ], sm=12, style={'align-items': 'center'})
                ] 
            ),
        ],
        flush=True,
        id = "accordion-individual"
    ),
)
