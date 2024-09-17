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

accordion_vs = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(title="Seguidores", children=
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
        id = "accordion-individual",
        style={"margin-right": "5px"}
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


# perfil geral
# titulo dos graficos com explicacao
# incluir no geral performance de conteudo (total de posts, total de engajamento, taxa de engajamento)

# individual
# conexoes com mais detalhes
# conteudo
# total de posts (plataforma)



accordion_pc = html.Div(
    dbc.Accordion(
        flush=True, id = "accordion-conteudo", children=
        [
            dbc.AccordionItem(title="📅 Completo", item_id="post-completo", children=[
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id = "grafico-posts-semana5", figure=fig, style={"height": "50vh"})
                    ], sm=12),
                ])
            ]),
            dbc.AccordionItem(title="📅 14-20 Março/2024", item_id="post-semana1", children=[
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id = "grafico-posts-semana5", figure=fig, style={"height": "50vh"})
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








