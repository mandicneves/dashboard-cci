# Componentes web
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# auxiliares
from app import *
from pages import geral, individual, tabs
import sidebar
import funcs

# Tratamento dados
import pandas as pd
import numpy as np
import json

# Graficos
import plotly.express as px
import plotly.graph_objects as go
from dash_bootstrap_templates import load_figure_template
tema = "cyborg"
load_figure_template(tema)

# =================================== #
# DADOS
# =================================== #

infos = pd.read_csv("./dataset/infos.csv")
local = pd.read_csv("./dataset/local.csv").dropna()
lat_mean = local.loc[local["CIDADE"] == "São Paulo", "LATITUDE"].iloc[0]
lon_mean = local.loc[local["CIDADE"] == "São Paulo", "LONGITUDE"].iloc[0]
seguidores = pd.read_csv("./dataset/seguidores.csv")
idade = pd.read_csv("./dataset/idade.csv")
genero = pd.read_csv("./dataset/genero.csv")
posts = pd.read_csv("./dataset/posts.csv")
with open('dataset/conexoes.json', 'r') as file:
    conexao = json.load(file)

# =================================== #
# LAYOUT
# =================================== #

cores = funcs.gerar_cores(len(sidebar.politicos))

cores_personalizadas = {}
for i in range(len(cores)):
    cores_personalizadas[sidebar.politicos[i]["value"]] = cores[i]

conexao_stylesheet = [{
    'selector': 'node',
    'style': {
        'label': 'data(label)',
        'text-valign': 'center',
        'text-halign': 'center',
        'color': 'rgb(255, 255, 255)',
        "background-color": 'data(color)',
        'border-color': 'white',
        'border-width': 1.5,
        "border-opacity": 1,
        'width': 'data(size)',
        'height': 'data(size)',
        'opacity': 0.90,
        'text-wrap': 'wrap',
        'text-max-width': 80,
        'font-weight': 'bold',
    }
}, {
    'selector': 'edge',
    'style': {
        "line-fill": "linear-gradient",
        'width': 2.5,
        'curve-style': 'bezier',
        'source-endpoint': 'outside-to-node',
        'target-endpoint': 'outside-to-node'
    }
}]

app.layout = html.Div([

    dbc.Row([
        dbc.Col([        
            dcc.Location(id="base-url"),
            sidebar.layout
        ], sm=2),
        dbc.Col([
            html.Div([
            ], id="page-content")
        ], sm=10)
    ]),


])

# =================================== #
# CALLBACKS
# =================================== #

@app.callback(
    [
        Output("page-content", "children"),
        Output("button-geral", "active"),
        Output("button-individual", "active"),
        Output("quadro-informacoes-div", "hidden"),
        Output("escolha-politico-div", "hidden"),
    ],
    Input("base-url", "pathname")
    )
def render_page(pathname):
    if pathname == "/":
        return geral.layout, True, False, False, True
    else:
        return individual.layout, False, True, True, False

@app.callback(
        Output("content", "children"), 
        [Input("tabs", "active_tab")]
        )
def switch_tab(at):
    if at == "tab-geral":
        return tabs.visao_geral
    elif at == "tab-metricas":
        return tabs.metricas_analise
    else:
        return tabs.conteudo

@app.callback(
        [
            Output("nome-politico", "children"),
            Output("idade-politico", "children"),
            Output("cidade-politico", "children"),
            Output("cargo-politico", "children"),
            Output("dropdown-politico", "value"),
            Output("imagem-politico", "src"),
        ],
    Input('dropdown-politico', 'value'),
    )
def update_info_politico(selected):

    if selected is None:

        nome = infos.loc[0, "NOME"]
        idade = infos.loc[0, "IDADE"]
        cidade = infos.loc[0, "CIDADE"]
        cargo = infos.loc[0, "CARGO + PARTIDO"]
        selected = infos.loc[0, "NOME"]

        return nome, idade, cidade, cargo, selected, "assets/images/@abiliobrunini.jpeg"
    
    dff = infos[infos["NOME"] == selected]
    nome= dff["NOME"].values[0]
    idade = dff["IDADE"].values[0]
    cidade = dff["CIDADE"].values[0]
    cargo = dff["CARGO + PARTIDO"].values[0]
    nick = dff["NICK"].values[0]
    imagem = f"assets/images/{nick}.jpeg"

    return nome, idade, cidade, cargo, nome, imagem

@app.callback(
        [
            Output('checklist-politicos-geral', 'value'),
            # Output('teste', 'children'),
        ],
    Input('checklist-politicos-geral', 'value'),
    )
def update_checklist(selected_values):
    # Ordena os valores selecionados
    selected_values = sorted(selected_values)
    
    # Lista de políticos e opções disponíveis
    politicos = [pol['value'] for pol in sidebar.politicos]
    opcoes = sidebar.opcoes

    # Caso todas as opções estejam selecionadas
    if selected_values == opcoes:
        return [selected_values]

    # Se "Todos" estiver selecionado
    if "Todos" in selected_values:
        # Se o número de selecionados for menor que o número total de políticos, retorna todas as opções
        if len(selected_values) < len(politicos):
            return [opcoes]
        else:
            # Remove "Todos" da seleção e retorna o restante
            selected_values.remove("Todos")
            return [selected_values]

    # Se "Todos" não estiver selecionado
    else:
        # Se todos os políticos estiverem selecionados, adiciona "Todos"
        if selected_values == politicos:
            selected_values.append("Todos")
            return [selected_values]
        else:
            # Retorna apenas os valores selecionados
            return [selected_values]

@app.callback(
    [
        Output("grafico-seguidores-geral", "figure"),
        Output("grafico-genero-geral", "figure"),
        Output("grafico-idade-geral", "figure"),
        Output("grafico-autenticos-geral", "figure"),
        Output("grafico-mapa-geral", "figure"),
    ],
    [
        Input('checklist-politicos-geral', 'value'),
        Input('radio-items-geral', 'value'),
    ]
    )
def update_graficos_geral(selected_values, operacao):

    px.set_mapbox_access_token(open("./keys/mapbox_token").read())
        
    df_seguidores = seguidores[seguidores["NOME"].isin(list(selected_values))]
    df_idade = idade[idade["NOME"].isin(list(selected_values))].groupby(["NOME", "IDADE"])
    df_genero = genero[genero["NOME"].isin(list(selected_values))].groupby(["NOME", "GENERO"])
    df_mapa = local[local["NOME"].isin(list(selected_values))]

    if operacao == "percentual":
        
        totais = df_seguidores[df_seguidores["PLATAFORMA"] == "TOTAL"][["NOME", "SEGUIDORES"]].set_index("NOME")
        df_autenticos = df_seguidores.groupby("NOME")["SEGUIDORES AUTÊNTICOS"].unique().explode().reset_index()
        df_seguidores = df_seguidores[df_seguidores["PLATAFORMA"] != "TOTAL"]
        df_seguidores = df_seguidores.join(totais, on="NOME", rsuffix='_TOTAL')
        df_seguidores["PERCENTUAL"] = df_seguidores["SEGUIDORES"] / df_seguidores["SEGUIDORES_TOTAL"]
        df_idade = df_idade["% SEGUIDORES IDADE"].mean().reset_index()
        df_genero = df_genero["% SEGUIDORES GENERO"].mean().reset_index()

        
        grafico_seguidores = px.bar(df_seguidores, x = "PLATAFORMA", y = "PERCENTUAL", color="NOME", barmode="group", color_discrete_map=cores_personalizadas)
        grafico_idade = px.bar(df_idade, x = "IDADE", y = "% SEGUIDORES IDADE", color="NOME", barmode="group", color_discrete_map=cores_personalizadas)
        grafico_genero = px.bar(df_genero, x = "GENERO", y = "% SEGUIDORES GENERO", color="NOME", barmode="group", color_discrete_map=cores_personalizadas)
        grafico_autenticos = px.bar(df_autenticos, y = "NOME", x = "SEGUIDORES AUTÊNTICOS", color="NOME", barmode="group", color_discrete_map=cores_personalizadas, orientation="h")
        mapa = px.scatter_mapbox(df_mapa, lat = "LATITUDE", lon = "LONGITUDE", color = "NOME", size = "% SEGUIDORES CIDADE", zoom = 10, opacity=0.6, 
                                hover_data={'CIDADE': True, "LATITUDE": False, "LONGITUDE": False}, color_discrete_map=cores_personalizadas)
            
    else:

        df_autenticos = df_seguidores[df_seguidores["PLATAFORMA"] == "TOTAL"]
        df_autenticos["SEGUIDORES AUTÊNTICOS"] = df_autenticos["SEGUIDORES AUTÊNTICOS"] * df_autenticos["SEGUIDORES"]
        df_idade = df_idade["SEGUIDORES IDADE"].sum().reset_index()
        df_genero = df_genero["SEGUIDORES GENERO"].sum().reset_index()

        grafico_seguidores = px.bar(df_seguidores, x = "PLATAFORMA", y = "SEGUIDORES", color="NOME", barmode="group", color_discrete_map=cores_personalizadas)
        grafico_idade = px.bar(df_idade, x = "IDADE", y = "SEGUIDORES IDADE", color="NOME", barmode="group", color_discrete_map=cores_personalizadas)
        grafico_genero = px.bar(df_genero, x = "GENERO", y = "SEGUIDORES GENERO", color="NOME", barmode="group", color_discrete_map=cores_personalizadas)
        grafico_autenticos = px.bar(df_autenticos, y = "NOME", x = "SEGUIDORES AUTÊNTICOS", color="NOME", barmode="group", color_discrete_map=cores_personalizadas, orientation="h")
        mapa = px.scatter_mapbox(df_mapa, lat = "LATITUDE", lon = "LONGITUDE", color = "NOME", size = "SEGUIDORES CIDADE", zoom = 10, opacity=0.6, 
                                hover_data={'CIDADE': True, "LATITUDE": False, "LONGITUDE": False}, color_discrete_map=cores_personalizadas)

    grafico_seguidores.update_layout(margin=go.layout.Margin(l=150, r=5, t=20, b=0), template = tema, showlegend = True, 
                                     yaxis=dict(side="right"), legend=dict(x=0, xanchor='right', y=1))
    grafico_idade.update_layout(margin=go.layout.Margin(l=5, r=5, t=10, b=0), template = tema, showlegend = False)
    grafico_genero.update_layout(margin=go.layout.Margin(l=5, r=5, t=10, b=0), template = tema, showlegend = False)
    grafico_autenticos.update_layout(margin=go.layout.Margin(l=5, r=5, t=10, b=0), template = tema, showlegend = False)
    mapa.update_layout(margin=go.layout.Margin(l=5, r=5, t=20, b=0), template = tema, showlegend = False,
                       mapbox = dict(center=go.layout.mapbox.Center(lat = lat_mean, lon = lon_mean)))    

    return grafico_seguidores, grafico_genero, grafico_idade, grafico_autenticos, mapa

@app.callback(
    [
        Output("grafico-idade-individual", "figure"),
        Output("grafico-genero-individual", "figure"),
    ],
        Input('dropdown-politico', 'value'),
)
def update_graficos_visao_geral(selected_value):

    df_idade = idade[idade["NOME"] == selected_value]
    df_genero = genero[genero["NOME"] == selected_value]

    plataformas = df_genero["PLATAFORMA"].unique().tolist()

    cores = px.colors.sequential.Viridis
    cores_personalizadas = {}
    for i in range(len(plataformas)):
        cores_personalizadas[plataformas[i]] = cores[i+1]


    grafico_genero = go.Figure()

    intervalos = [
        [0.05, 0.2],
        [0.3, 0.45],
        [0.55, 0.7],
        [0.8, 0.95],
    ]

    for idx, plataforma in enumerate(plataformas):

        labels = df_genero.loc[df_genero["PLATAFORMA"] == plataforma, "GENERO"]
        values = df_genero.loc[df_genero["PLATAFORMA"] == plataforma, "SEGUIDORES GENERO"]
        colors = [funcs.ajustar_intensidade(cores_personalizadas[plataforma], i) for i in [1.3, 0.7]]

        grafico_genero.add_trace(go.Pie(
            labels=labels,
            values=values,
            hole=0.5,
            name=plataforma,
            textinfo='percent',
            domain=dict(x=intervalos[idx]),
            marker=dict(colors=colors),
            showlegend=False
        ))

    eixo_x = [
        {'text': 'INSTAGRAM', 'x': 0.078, 'y': 0.05, 'font_size': 20, 'showarrow': False},
        {'text': 'X', 'x': 0.375, 'y': 0.05, 'font_size': 20, 'showarrow': False},
        {'text': 'TIKTOK', 'x': 0.62, 'y': 0.05, 'font_size': 20, 'showarrow': False},
        {'text': 'YOUTUBE', 'x': 0.92, 'y': 0.05, 'font_size': 20, 'showarrow': False}
        ]

    grafico_idade = px.bar(df_idade, x = "IDADE", y = "% SEGUIDORES IDADE", color = "PLATAFORMA", barmode="group", color_discrete_map=cores_personalizadas)

    grafico_idade.update_layout(margin=go.layout.Margin(l=5, r=5, t=10, b=0), template = tema, showlegend = True)
    grafico_genero.update_layout(margin=go.layout.Margin(l=5, r=5, t=5, b=0), template = tema, showlegend = False, annotations=eixo_x)

    return grafico_idade, grafico_genero

@app.callback(
        [
            Output("grafico-conexoes-individual", "elements"),
            Output("grafico-conexoes-individual", "stylesheet"),
        ],
        Input('dropdown-politico', 'value'),
)
def updtate_conexoes(selected_value):

    elementos = conexao[selected_value]

    return elementos, conexao_stylesheet

# =================================== #
# RUN SERVER
# =================================== #

if __name__ == "__main__":
    app.run(debug=True)
