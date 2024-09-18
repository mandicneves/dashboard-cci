from dash import html, dcc
import dash_bootstrap_components as dbc

import pandas as pd

from app import *
import funcs

dados = pd.read_csv("./dataset/infos.csv")

politicos = [{"label": row["NICK"], "value": row["NOME"]} for i, row in dados.iterrows()]
opcoes = dados["NOME"].unique().tolist()
opcoes.insert(0, "Todos")


cores = funcs.gerar_cores(len(politicos))
cores_personalizadas = {}
for i in range(len(cores)):
    cores_personalizadas[politicos[i]["value"]] = cores[i]

style_sidebar = style={"box-shadow": "2px 2px 10px 0px rgba(10, 9, 7, 0.10)",
                    "margin": "10px",
                    "padding": "10px",
                    "height": "95vh"}

# ============================
# LAYOUT
# ============================

layout = dbc.Card(
    [   
        # BOTOES DE GERAL E INDIVIDUAL
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Geral", href="/", active=True, className="nav-link", id = "button-geral")),
                dbc.NavItem(dbc.NavLink("Individual", href="individual", className="nav-link", id = "button-individual")),
            ], pills=True, justified=True, style={"padding-top": "10px", "padding-bottom": "10px"}),        
        html.Hr(),
                




        # INFORMACOES NO QUADRO GERAL (GERAL)
        html.Div([
            html.H2("PROJETO CCI", style={'font-size': '1.5vw', 'padding-left': '10px', "padding-top": "10"}),
            html.P("Dashboard de análise do comportamento de políticos nas redes sociais", className="lead", 
                   style = {'font-size': '1vw', "padding": "10px", "text-align": "left"}),
            html.Hr(),
            dcc.RadioItems(
                options=[
                    {
                        "label":
                            [
                                html.Img(src="https://cdn-icons-png.flaticon.com/512/44/44908.png", height=15, style={"filter": "invert(1)"},
                                         id="img-percentual"),
                            ],
                        "value": "percentual",
                    },
                    {
                        "label":
                            [
                                html.Img(src="https://cdn-icons-png.flaticon.com/512/43/43492.png", height=15, style={"filter": "invert(1)"},
                                         id="img-absoluto"),
                            ],
                        "value": "absoluto",
                    },
                ],
                value="percentual", 
                inline=True,
                labelStyle={"padding": "5px", 'font-size': '0.8vw', "padding-left": "15px"},
                inputStyle={"margin-right": "10px"},
                id="radio-items-geral"
            ),
            dbc.Tooltip("Coloca os gráficos em valores porcentuais", target="img-percentual"),
            dbc.Tooltip("Coloca os gráficos em valores absolutos", target="img-absoluto"),
            html.Hr(),
            html.P("Perfis analisados", className="lead", 
               style = {'font-size': '1.25vw', "padding": "10px", "text-align": "left"}),
            dbc.Checklist(
                options=funcs.criar_opcoes(dados, cores_personalizadas),
                value=dados["NOME"].unique(),
                style = {"padding": "5px", 'font-size': '0.8vw'},
                id = "checklist-politicos-geral",
                className="custom-checklist"
                )
        ],id="quadro-informacoes-div", hidden=False),





        # MENU DE SELECAO DO POLITICO (INDIVIDUAL)
        html.Div([
            html.H4("Escolha um perfil", style={'font-size': '1.1vw', 'padding': '10px'}),
            dcc.Dropdown(
                options=politicos,
                value="Abilio Brunini",
                id="dropdown-politico"),
            html.Img(src = "https://upload.wikimedia.org/wikipedia/commons/f/f9/Foto_oficial_de_Luiz_In%C3%A1cio_Lula_da_Silva_%28ombros%29.jpg",
                     style={"width": "12vw", "display": "block", "padding-top": "10px", "margin": "0 auto", "margin-top": "10px"},
                     id="imagem-politico"),
            dbc.ListGroup([
                dbc.ListGroupItem(id="nome-politico", className="list-group-item-custom"),
                dbc.ListGroupItem(id="idade-politico", className="list-group-item-custom"),
                dbc.ListGroupItem(id="cidade-politico", className="list-group-item-custom"),
                dbc.ListGroupItem(id="cargo-politico", className="list-group-item-custom"),
                ], style={"padding": "0.5px", 'font-size': '1vw', 'margin-top': '15px'},
            )
        ], id="escolha-politico-div", hidden=True),                
    ], style=style_sidebar
)


