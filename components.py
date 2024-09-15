import dash_bootstrap_components as dbc
from dash import html, dcc

import plotly.graph_objects as go
from dash_bootstrap_templates import load_figure_template
tema = "cyborg"
load_figure_template(tema)

card_post1 = dbc.Card(
    [
        dbc.CardImg(src="https://dash-bootstrap-components.opensource.faculty.ai/static/images/placeholder286x180.png", top=True),
        dbc.CardBody(
            [
                html.H4(id = "plataforma-post1"),

                dbc.Row([
                    dbc.Col([
                        html.I(className="fas fa-heart", style={"color": "#FF5555"}),
                        html.Span(id="likes-post1")
                    ]),
                    dbc.Col([
                        html.I(className="fas fa-comment", style={"color": "#66D9EF"}),
                        html.Span(id="likes-post1")
                    ]),
                ], style={"padding": "10px"}),

                dbc.Row([
                    dbc.Col([
                        html.I(className="fas fa-comment-dots", style={"color": "#AAAAAA"}),
                        html.Span(id="likes-post1")
                    ]),
                    dbc.Col([
                        html.I(className="fas fa-thumbs-up", style={"color": "#E78C45"}),
                        html.Span(id="likes-post1")
                    ]),
                ], style={"padding": "10px"}),

                dbc.Row([
                    dbc.Col([
                        html.I(className="fas fa-chart-line", style={"color": "#A6E22E"}),
                        html.Span(id="likes-post1")
                    ]),
                    dbc.Col([
                        html.I(className="fas fa-share", style={"color": "#AE81FF"}),
                        html.Span(id="likes-post1")
                    ]),
                ], style={"padding": "10px"}),
                
                html.Div(
                    [
                    dbc.Button("Ir para Post", outline=True, color="primary", style={"margin-top": "10px"}),
                    ], className="d-grid gap-2",
                )
            ]
        ),
    ],
)

card_post2 = dbc.Card(
    [
        dbc.CardImg(src="https://dash-bootstrap-components.opensource.faculty.ai/static/images/placeholder286x180.png", top=True),
        dbc.CardBody(
            [
                html.H4(id = "plataforma-post2"),

                dbc.Row([
                    dbc.Col([
                        html.I(className="fas fa-heart", style={"color": "#FF5555"}),
                        html.Span(id="likes-post2")
                    ]),
                    dbc.Col([
                        html.I(className="fas fa-comment", style={"color": "#66D9EF"}),
                        html.Span(id="likes-post2")
                    ]),
                ], style={"padding": "10px"}),

                dbc.Row([
                    dbc.Col([
                        html.I(className="fas fa-comment-dots", style={"color": "#AAAAAA"}),
                        html.Span(id="likes-post2")
                    ]),
                    dbc.Col([
                        html.I(className="fas fa-thumbs-up", style={"color": "#E78C45"}),
                        html.Span(id="likes-post2")
                    ]),
                ], style={"padding": "10px"}),

                dbc.Row([
                    dbc.Col([
                        html.I(className="fas fa-chart-line", style={"color": "#A6E22E"}),
                        html.Span(id="likes-post2")
                    ]),
                    dbc.Col([
                        html.I(className="fas fa-share", style={"color": "#AE81FF"}),
                        html.Span(id="likes-post2")
                    ]),
                ], style={"padding": "10px"}),
                
                html.Div(
                    [
                    dbc.Button("Ir para Post", outline=True, color="primary", style={"margin-top": "10px"}),
                    ], className="d-grid gap-2",
                )
            ]
        ),
    ],
)

card_post3 = dbc.Card(
    [
        dbc.CardImg(src="https://dash-bootstrap-components.opensource.faculty.ai/static/images/placeholder286x180.png", top=True),
        dbc.CardBody(
            [
                html.H4(id = "plataforma-post3"),

                dbc.Row([
                    dbc.Col([
                        html.I(className="fas fa-heart", style={"color": "#FF5555"}),
                        html.Span(id="likes-post3")
                    ]),
                    dbc.Col([
                        html.I(className="fas fa-comment", style={"color": "#66D9EF"}),
                        html.Span(id="likes-post3")
                    ]),
                ], style={"padding": "10px"}),

                dbc.Row([
                    dbc.Col([
                        html.I(className="fas fa-comment-dots", style={"color": "#AAAAAA"}),
                        html.Span(id="likes-post3")
                    ]),
                    dbc.Col([
                        html.I(className="fas fa-thumbs-up", style={"color": "#E78C45"}),
                        html.Span(id="likes-post3")
                    ]),
                ], style={"padding": "10px"}),

                dbc.Row([
                    dbc.Col([
                        html.I(className="fas fa-chart-line", style={"color": "#A6E22E"}),
                        html.Span(id="likes-post3")
                    ]),
                    dbc.Col([
                        html.I(className="fas fa-share", style={"color": "#AE81FF"}),
                        html.Span(id="likes-post3")
                    ]),
                ], style={"padding": "10px"}),
                
                html.Div(
                    [
                    dbc.Button("Ir para Post", outline=True, color="primary", style={"margin-top": "10px"}),
                    ], className="d-grid gap-2",
                )
            ],
        ),
    ],
)

fig = go.Figure()
fig.update_layout(template = tema)