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

# =================================== #
# COMPONENTES PARA LAYOUT GERAL
# =================================== #

tabs_geral = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Visão Geral", tab_id="tab-geral-visaogeral"),
                dbc.Tab(label="Performance de Conteúdo", tab_id="tab-geral-conteudo")
            ],
            id="tabs-geral",
            active_tab="tab-geral-visaogeral",
            style={"padding": "10px", "margin": "10px"}
        ),
        html.Div(id="geral-content"),
    ],
)

seguidores_geral = html.Div([
    # primeira linha
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="grafico-seguidores-geral", figure=fig, style={"height": "28vh", "padding": "5px"})
        ], sm=8),
        dbc.Col([
            dcc.Graph(id="grafico-genero-geral", figure=fig, style={"height": "28vh", "padding": "5px", "margin-right": "20px"})
        ], sm=4),
    ], className="g-0"),


    # segunda linha
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="grafico-idade-geral", figure=fig, style={"height": "28vh", "padding": "5px", "margin-right": "20px"})
        ], sm=12)
    ]),



    # terceira linha
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="grafico-autenticos-geral", figure=fig, style={"height": "30vh", "padding": "5px"})
        ], sm = 6),       
        dbc.Col([
            dcc.Graph(id="grafico-mapa-geral", figure=fig, style={"height": "30vh", "padding": "5px", "margin-right": "20px"})
        ], sm = 6),        
    ], className="g-0")    
])

perfomance_conteudo = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="grafico-geral-total-posts", figure=fig, style={"height": "42vh", "padding": "5px"}),
        ], sm=6),
        dbc.Col([
            dcc.Graph(id="grafico-geral-total-engajamento", figure=fig, style={"height": "42vh", "padding": "5px", "margin-right": "10px"}),            
        ], sm=6),
    ], className="g-0"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="grafico-geral-taxa-engajamento", figure=fig, style={"height": "42vh", "padding": "5px"})
        ], sm=6),
        dbc.Col([
            dcc.Graph(id="grafico-geral-vmg", figure=fig, style={"height": "42vh", "padding": "5px", "margin-right": "10px"})
        ], sm=6),
        html.Div([
            dbc.Popover(
                [
                    dbc.PopoverHeader("Total de Posts", style={"background-color": "#45A1FF"}),
                    dbc.PopoverBody("Soma das postagens realizadas no período."),
                ],
                target="grafico-geral-total-posts", trigger="click", id="dica-total-posts"),
            dbc.Popover(
                [
                    dbc.PopoverHeader("Total de Engajamento", style={"background-color": "#45A1FF"}),
                    dbc.PopoverBody("Engajamento é o número de vezes que o público engajou com a publicação curtindo, comentando ou compartilhando."),
                ],
                target="grafico-geral-total-engajamento", trigger="click", id="dica-total-engajamento"),
            dbc.Popover(
                [
                    dbc.PopoverHeader("Taxa de Engajamento", style={"background-color": "#45A1FF"}),
                    dbc.PopoverBody("Taxa de engajamento é o percentual do público que engajou com a publicação curtindo, comentando ou compartilhando."),
                ],
                target="grafico-geral-taxa-engajamento", trigger="click", id="dica-taxa-engajamento"),
            dbc.Popover(
                [
                    dbc.PopoverHeader("Total de VMG", style={"background-color": "#45A1FF"}),
                    dbc.PopoverBody("VMG (Valor de Mídia Ganho) é um valor monetário estimado da publicação com base no tamanho do público alcançado."),
                ],
                target="grafico-geral-vmg", trigger="click", id="dica-vmg"),
                ])               
    ], className="g-0"),
])







# =================================== #
# COMPONENTES PARA LAYOUT INDIVIDUAL
# =================================== #

# Lista de cores, do valor mais alto (escuro) ao valor mais baixo (claro)
cores = ['#2f003a', '#58016d', '#8802a8', '#aa02d2', '#321c54', 
         '#5d349c', '#9050f0', '#b464ff', '#2b335f', '#505eb2']

# Texto representando os valores relativos (do maior ao menor)
valores = [f'' for i in range(len(cores))]
valores = ["Máx", "", "", "", "", "", "", "", "", "Mín"]

# Criar uma div para cada cor e valor, organizando-os em uma legenda
legenda = html.Div(
    children=[
        html.Div(
            style={'backgroundColor': cor, 'height': '4vh', 'width': '7vw', 'margin': '0px', 'display': 'inline-block'},
            children=html.Span(texto, style={'color': '#bfbfbf', 'paddingLeft': '5px'})
        ) for cor, texto in zip(cores, valores)],
    
    style={
        'display': 'flex',
        'flexDirection': 'column',
        'justifyContent': 'center',  # Centraliza verticalmente
        'alignItems': 'center',       # Centraliza horizontalmente os itens internos
        'margin-top': '60px',
        'textAlign': 'center'
    }   
)





button_group1 = dbc.ButtonGroup(
    [dbc.Button("Insta", id="insta-politico", outline=True, color="secondary", style={"fontSize": "1vw"}, size="sm"), 
     dbc.Button("Twitter", id="twitter-politico", outline=True, color="secondary", style={"fontSize": "1vw"}, size="sm")],
     style={"margin-top": "10px"}
)
button_group2 = dbc.ButtonGroup(
    [dbc.Button("TikTok", id="tiktok-politico", outline=True, color="secondary", style={"fontSize": "1vw"}, size="sm"), 
     dbc.Button("YouTube", id="youtube-politico", outline=True, color="secondary", style={"fontSize": "1vw"}, size="sm")]
)

list_group = dbc.ListGroup(
    [
        dbc.ListGroupItem(
            [
                html.Div(
                    [
                        html.H5("Conexão selecionada", className="mb-1"),
                    ],
                    className="d-flex w-100 justify-content-between",
                ),
                html.P(id="conexao-selecionada", className="mb-1"),
            ],
            style={"margin-top": "30px"}
        ),
        dbc.ListGroupItem(
            [
                html.Div(
                    [
                        html.H5("Total de Engajamento", className="mb-1"),
                    ],
                    className="d-flex w-100 justify-content-between",
                ),
                html.P(id="engajamento-conexao-selecionada", className="mb-1"),
            ]
        ),
        dbc.ListGroupItem(
            [
                html.Div(
                    [
                        html.H5("Total de Posts", className="mb-1"),
                    ],
                    className="d-flex w-100 justify-content-between",
                ),
                html.P(id="posts-conexao-selecionada", className="mb-1"),
            ]
        ),
        dbc.ListGroupItem(
            [
                html.Div(
                    [
                        html.H5("Top Post", className="mb-1"),
                    ],
                    className="d-flex w-100 justify-content-between",
                ),
                html.Div([
                    dbc.Button(children="Link", id="link-conexao-selecionada", outline=True, color="secondary")
                    ], className="d-grid gap-2")
                
            ]
        ),
    ]
)

accordion_vs = html.Div(
    dbc.Accordion(
        [   
            # Accordion com infos dos seguidores
            dbc.AccordionItem(
                item_id="seguidores-accordion",
                title="Seguidores", children=
                [
                    dbc.Row([
                        dbc.Col([dcc.Graph(id="grafico-seguidores-individual", figure=fig, style={"height": "32vh", "margin-top": "5px", "margin-right": "10px"}),], sm=4),
                        dbc.Col([dcc.Graph(id="grafico-idade-individual", figure=fig, style={"height": "32vh", "margin-top": "5px"}),], sm=8),
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col([dcc.Graph(id="grafico-genero-individual", figure=fig, style={"height": "35vh", "margin-top": "15px", "margin-right": "10px"}),],sm=7),
                        dbc.Col([dcc.Graph(id="grafico-mapa-individual", figure=fig, style={"height": "35vh", "margin-top": "15px"}),],sm=5),
                    ], className="g-0"),
                    
                    
                ] 
            ),
            # Accordion com info das conexoes
            dbc.AccordionItem(
                item_id="conexao-accordion",
                title="Conexões", children=
                [
                    dbc.Col([
                        html.Div([
                            dbc.Row([
                                dbc.Col(
                                    [legenda]
                                    , sm=1),
                                dbc.Col([
                                    cyto.Cytoscape(
                                        id="grafico-conexoes-individual",
                                        layout={"name": "cola"},
                                        style={"height": "65vh"})
                                ], sm=8),
                                # ], id="grafico-conexoes-individual", sm=9),
                                dbc.Col([
                                    dbc.Card([
                                        list_group
                                    ],
                                    style={"margin-top": "30px", "margin-right": "10px", "padding": "10px", "height": "60vh"})
                                ], sm=3),
                            ])
                        ])
                    ], sm=12, style={'align-items': 'center'})
                ] 
            ),
        ],
        flush=True,
        id = "accordion-individual",
        style={"margin-right": "5px"},
    ),
)

accordion_pc = html.Div(
    dbc.Accordion(
        flush=True, id = "accordion-conteudo", active_item="post-completo",children=
        [   
            # PERIODO COMPLETO
            dbc.AccordionItem(title="📅 14 Março - 30 Setembro/2024", item_id="post-completo", children=[
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id = "grafico-total-posts-final", figure=fig, style={"height": "30vh", "margin-right": "10px"}),
                    ], sm=6),
                    dbc.Col([
                        dcc.Graph(id = "grafico-engajamento-total-final", figure=fig, style={"height": "30vh"}),
                    ], sm=6),
                ], className="g-0"),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id = "grafico-engajamento-taxa-final", figure=fig, style={"height": "30vh", "margin-right": "10px", "margin-top": "10px"}),
                    ], sm=6),
                    dbc.Col([
                        dcc.Graph(id = "grafico-vmg-final", figure=fig, style={"height": "30vh", "margin-top": "10px"}),
                    ], sm=6),
                ], className="g-0"),
            ]),
            # SEMANA 1
            dbc.AccordionItem(title="📅 14-20 Março/2024", item_id="post-semana1", children=[
                html.Div([], id="top-posts-semana1", hidden=True),
                html.Div([], id="graficos-semana1", hidden=False),
            ]),
            # SEMANA 2
            dbc.AccordionItem(title="📅 04-10 Setembro/2024", item_id="post-semana2", children=[
                html.Div([], id="top-posts-semana2", hidden=True),
                html.Div([], id="graficos-semana2", hidden=False),
            ]),
        ]
    ),
    
)

