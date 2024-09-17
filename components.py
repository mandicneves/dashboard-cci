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
            dcc.Graph(id="grafico-geral-total-posts", figure=fig, style={"height": "28vh", "padding": "5px", "margin-right": "15px"})
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="grafico-geral-total-engajamento", figure=fig, style={"height": "28vh", "padding": "5px", "margin-right": "15px"})
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="grafico-geral-taxa-engajamento", figure=fig, style={"height": "28vh", "padding": "5px", "margin-right": "15px"})
        ])
    ]),

])















# =================================== #
# COMPONENTES PARA LAYOUT INDIVIDUAL
# =================================== #

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
                        dbc.Col([dcc.Graph(id="grafico-idade-individual", figure=fig, style={"height": "30vh", "margin-top": "5px"}),], sm=12)
                    ]),
                    dbc.Row([
                        dbc.Col([dcc.Graph(id="grafico-genero-individual", figure=fig, style={"height": "35vh", "margin-top": "15px"}),],sm=7),
                        dbc.Col([dcc.Graph(id="grafico-mapa-individual", figure=fig, style={"height": "35vh", "margin-top": "15px"}),],sm=5),
                    ]),
                    
                    
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
                                dbc.Col([
                                    # html.Div(id="cytoscape"),
                                    cyto.Cytoscape(
                                        id="grafico-conexoes-individual",
                                        layout={"name": "cola"},
                                        style={"height": "65vh"})
                                ], sm=9),
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

def make_postcard(i):

    post_card = dbc.Card(
        [
            dbc.CardImg(src="", top=True, style={"height": "40%"}),  # Substitua pelo caminho da sua imagem
            dbc.CardBody(
                [
                    # Primeira linha
                    dbc.Row(
                        [
                            dbc.Col(html.Div("❤️", id=f"likes-{i}"), width=6),  # Emoji de coração
                            dbc.Col(html.Div("💬", id=f"comentarios-{i}"), width=6),  # Emoji de comentário
                        ],
                        className="mb-2",
                    ),
                    # Segunda linha
                    dbc.Row(
                        [
                            dbc.Col(html.Div("💭", id=f"impressoes-{i}"), width=6),  # Emoji de balão de pensamento
                            dbc.Col(html.Div("📈", id=f"lift-conteudo-{i}"), width=6),  # Emoji de gráfico de linha ascendente
                        ],
                        className="mb-2",
                    ),
                    # Terceira linha
                    dbc.Row(
                        [
                            dbc.Col(html.Div("👍", id=f"taxa-engajamento-{i}"), width=6),  # Emoji de dedo polegar
                            dbc.Col(html.Div("🔄", id=f"compartilhamentos-{i}"), width=6),  # Emoji de seta de compartilhamento
                        ],
                        className="mb-2"
                    ),
                    html.Div([
                        # Botão no final do card
                        dbc.Button(
                            "Post", color="primary", outline=True, id=f"link-post-{i}"
                        ),                    
                    ], className="d-grid gap-2", style={"margin-top": "20px"})

                ]
            ),
        ],
        style={
            "height": "30vh",  # Ajuste a altura do card
        },
    )


    return post_card

accordion_pc = html.Div(
    dbc.Accordion(
        flush=True, id = "accordion-conteudo", children=
        [
            dbc.AccordionItem(title="📅 14 Março - 30 Setembro/2024", item_id="post-completo", children=[
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id = "grafico-posts-final", figure=fig, style={"height": "50vh"})
                    ], sm=12),
                ])
            ]),
            dbc.AccordionItem(title="📅 14-20 Março/2024", item_id="post-semana1", children=[
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id = "grafico-posts-semana1", figure=fig, style={"height": "50vh"})
                    ], sm=6),
                    dbc.Col([
                        html.Div(
                            [
                                html.H5("Top 3 posts"),
                                html.Hr(style={"margin-bottom": "20px"}),
                                dbc.Row(
                                    [dbc.Col(make_postcard(i), sm=4) for i in range(1,4)]
                                )
                            ],
                            className="h-100 p-5 text-white bg-secondary rounded-3"
                        )
                    ], sm=6),
                ])
            ]),








        ]
    ),
    
)

