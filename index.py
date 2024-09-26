# Componentes web
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# auxiliares
from app import *
from pages import geral, individual, tabs
import sidebar
import funcs
import components
import time

# Tratamento dados
import pandas as pd
import numpy as np
import json

# Graficos
import plotly.express as px
import plotly.graph_objects as go
from dash_bootstrap_templates import load_figure_template
import dash_cytoscape as cyto
tema = "cyborg"
load_figure_template(tema)
cyto.load_extra_layouts()

# =================================== #
# DADOS
# =================================== #

infos = pd.read_csv("./dataset/infos.csv")
local = pd.read_csv("./dataset/local.csv").dropna()
local["PLATAFORMA"] = local["PLATAFORMA"].str.replace("X", "TWITTER")
lat_mean = local.loc[local["ESTADO"] == "São Paulo", "LATITUDE"].iloc[0]
lon_mean = local.loc[local["ESTADO"] == "São Paulo", "LONGITUDE"].iloc[0]
seguidores = pd.read_csv("./dataset/seguidores.csv")
seguidores["PLATAFORMA"] = seguidores["PLATAFORMA"].str.replace("X", "TWITTER")
idade = pd.read_csv("./dataset/idade.csv")
idade["PLATAFORMA"] = idade["PLATAFORMA"].str.replace("X", "TWITTER")
genero = pd.read_csv("./dataset/genero.csv")
genero["PLATAFORMA"] = genero["PLATAFORMA"].str.replace("X", "TWITTER")
posts = pd.read_csv("./dataset/posts.csv")
posts["Nome"] = posts["Nome"].str.replace("Josimar Maranhãozinho", "Josimar de Maranhãozinho")
conteudo = pd.read_csv("./dataset/conteudo.csv")
ordem = conteudo["Semana"].unique().tolist()
conteudo["Semana"] = pd.Categorical(conteudo["Semana"], ordered=True, categories=ordem)
conteudo["Data"] = pd.to_datetime(conteudo["Data"], dayfirst=True)
top_posts = pd.read_csv("./dataset/top_posts.csv")
top_posts["Legenda"] = top_posts["Legenda"].str.strip()
df_conexao = pd.read_csv("./dataset/df_conexoes.csv")
df_conexao["Metrica"] = (df_conexao["Engajamento"] / df_conexao["Total de Posts"]).astype(int)

with open('dataset/conexoes.json', 'r') as file:
    conexao = json.load(file)


# =================================== #
# LAYOUT
# =================================== #

cores = funcs.gerar_cores(len(sidebar.politicos))
cores_personalizadas = sidebar.cores_personalizadas

conexao_stylesheet = [{
    'selector': 'node',
    # ESTILO DAS BOLAS
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
        'opacity': 0.95,
        'text-wrap': 'wrap',
        'text-max-width': 80,
        'font-weight': 'bold',
    }
}, {
    'selector': 'edge',
    # ESTILO DAS LINHAS
    'style': {
        'opacity': 0.2,
        'width': 5,
        'curve-style': 'haystack',
        'source-endpoint': 'outside-to-node',
        'target-endpoint': 'outside-to-node',
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

# CARREGAR PAGINAS
@app.callback(
    [
        Output("page-content", "children"),
        Output("button-geral", "active"),
        Output("button-individual", "active"),
        Output("quadro-informacoes-div", "hidden"),
        Output("escolha-politico-div", "hidden"),
        Output("div-mostrar-posts", "hidden", allow_duplicate=True),
    ],
    [Input("base-url", "pathname")],
    prevent_initial_call=True
    )
def render_page(pathname):
    if pathname == "/":
        return geral.layout, True, False, False, True, True
    else:
        return individual.layout, False, True, True, False, True

# ALTERAR ENTRE TABS DO GERAL
@app.callback(
        Output("geral-content", "children"), 
        [Input("tabs-geral", "active_tab")]
        )
def switch_tab_geral(at):
    if at == "tab-geral-visaogeral":
        return components.seguidores_geral
    else:
        return components.perfomance_conteudo

# ALTERAR ENTRE TABS DO INDIVIDUAL
@app.callback(
        [
            Output("content", "children"),
        ], 
        [
            Input("tabs", "active_tab")
        ],
        )
def switch_tab_individual(at):
    if at == "tab-geral":
        return [tabs.visao_geral]
    else:
        return [tabs.conteudo]

# PAGINAL INDIVIDUAL CARREGANDO INFORMACOES PESSOAIS DOS POLITICOS
@app.callback(
        [
            Output("nome-politico", "children"),
            Output("idade-politico", "children"),
            Output("cidade-politico", "children"),
            Output("cargo-politico", "children"),
            Output("dropdown-politico", "value"),
            Output("imagem-politico", "src"),
            Output("insta-politico", "href"),
            Output("twitter-politico", "href"),
            Output("tiktok-politico", "href"),
            Output("youtube-politico", "href"),
        ],
    Input('dropdown-politico', 'value'),
    )
def update_info_politico(selected):

    # selected = "Abilio Brunini"

    if selected is None:

        nome = infos.loc[0, "NOME"]
        idade = infos.loc[0, "IDADE"]
        cidade = infos.loc[0, "CIDADE"]
        cargo = infos.loc[0, "CARGO + PARTIDO"]
        selected = infos.loc[0, "NOME"]
        insta = infos.loc[0, "INSTA"]
        x = infos.loc[0, "X"]
        tiktok = infos.loc[0, "TIKTOK"]
        youtube = infos.loc[0, "YOUTUBE"]

        return nome, idade, cidade, cargo, selected, "assets/images/@abiliobrunini.jpeg", insta, x, tiktok, youtube
    
    dff = infos[infos["NOME"] == selected]
    nome= dff["NOME"].values[0]
    idade = dff["IDADE"].values[0]
    cidade = dff["CIDADE"].values[0]
    cargo = dff["CARGO + PARTIDO"].values[0]
    nick = dff["NICK"].values[0]
    imagem = f"assets/images/{nick}.jpeg"
    insta = dff["INSTA"].values[0]
    x = dff["X"].values[0]
    tiktok = dff["TIKTOK"].values[0]
    youtube = dff["YOUTUBE"].values[0]

    return nome, idade, cidade, cargo, nome, imagem, insta, x, tiktok, youtube

# PAGINAL INDIVIDUAL TRATAMENTO DO CHECKLIST DE POLITICOS
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

# PAGINA GERAL - ABA VISAO GERAL
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
def update_graficos_geral_vs(selected_values, operacao):

    # chave api
    px.set_mapbox_access_token(open("./keys/mapbox_token").read())
    
    # filtrando datasets
    df_seguidores = seguidores[seguidores["NOME"].isin(list(selected_values))]
    df_idade = idade[idade["NOME"].isin(list(selected_values))].groupby(["NOME", "IDADE"])
    df_genero = genero[genero["NOME"].isin(list(selected_values))].groupby(["NOME", "GENERO"])
    df_mapa = local[local["NOME"].isin(list(selected_values))]

    # verificando qual a operacao se percentual ou absoluto
    if operacao == "percentual":
        
        totais = df_seguidores[df_seguidores["PLATAFORMA"] == "TOTAL"][["NOME", "SEGUIDORES"]].set_index("NOME")
        df_autenticos = df_seguidores.groupby("NOME")["SEGUIDORES AUTÊNTICOS"].unique().explode().reset_index()
        df_seguidores = df_seguidores[df_seguidores["PLATAFORMA"] != "TOTAL"]
        df_seguidores = df_seguidores.join(totais, on="NOME", rsuffix='_TOTAL')
        df_seguidores["PERCENTUAL"] = round(df_seguidores["SEGUIDORES"] / df_seguidores["SEGUIDORES_TOTAL"], 3)
        df_idade = df_idade["% SEGUIDORES IDADE"].mean().reset_index()
        df_genero = df_genero["% SEGUIDORES GENERO"].mean().reset_index()
        df_mapa = df_mapa.groupby(["NOME", "ESTADO"])["% SEGUIDORES ESTADO"].mean().reset_index()
        df_mapa = df_mapa.merge(local[["LATITUDE", "LONGITUDE", "ESTADO", "NOME"]], on=["ESTADO", "NOME"])
        df_mapa["% SEGUIDORES ESTADO"] = round(df_mapa["% SEGUIDORES ESTADO"] * 100, 1)

        
        grafico_seguidores = px.bar(df_seguidores, x = "PLATAFORMA", y = "PERCENTUAL", color="NOME", barmode="group", color_discrete_map=cores_personalizadas)
        grafico_seguidores.update_yaxes(tickformat=".1%")
        grafico_idade = px.bar(df_idade, x = "IDADE", y = "% SEGUIDORES IDADE", color="NOME", barmode="group", color_discrete_map=cores_personalizadas)
        grafico_idade.update_yaxes(tickformat=".1%")
        grafico_genero = px.bar(df_genero, x = "GENERO", y = "% SEGUIDORES GENERO", color="NOME", barmode="group", color_discrete_map=cores_personalizadas)
        grafico_genero.update_yaxes(tickformat=".1%")
        grafico_autenticos = px.bar(df_autenticos, x = "NOME", y = "SEGUIDORES AUTÊNTICOS", color="NOME", color_discrete_map=cores_personalizadas)
        grafico_autenticos.update_xaxes(showticklabels=False)
        grafico_autenticos.update_yaxes(tickformat=".1%")
        mapa = px.scatter_mapbox(df_mapa, lat = "LATITUDE", lon = "LONGITUDE", color = "NOME", size = "% SEGUIDORES ESTADO", zoom = 10, opacity=0.6, 
                                hover_data={'ESTADO': True, "LATITUDE": False, "LONGITUDE": False}, color_discrete_map=cores_personalizadas)  

        titulo_seguidores = "Percentual (%) de seguidores por plataforma"
        titulo_idade = "Percentual (%) médio de seguidores por idade"
        titulo_genero = "Percentual (%) médio de seguidores por gênero"
        titulo_autenticos = "Percentual (%) de seguidores autênticos"
        titulo_mapa = "Percentual (%) médio de seguidores por estado"

    else:

        df_autenticos = df_seguidores.loc[df_seguidores["PLATAFORMA"] == "TOTAL", :].reset_index(drop=True)
        df_autenticos["SEGUIDORES AUTÊNTICOS"] = df_autenticos["SEGUIDORES AUTÊNTICOS"] * df_autenticos["SEGUIDORES"]
        df_idade = df_idade["SEGUIDORES IDADE"].sum().reset_index()
        df_genero = df_genero["SEGUIDORES GENERO"].sum().reset_index()
        df_mapa = df_mapa.groupby(["NOME", "ESTADO"])["SEGUIDORES ESTADO"].sum().reset_index()
        df_mapa = df_mapa.merge(local[["LATITUDE", "LONGITUDE", "ESTADO", "NOME"]], on=["ESTADO", "NOME"])
        df_mapa["SEGUIDORES ESTADO"] = round(df_mapa["SEGUIDORES ESTADO"], 0)


        grafico_seguidores = px.bar(df_seguidores, x = "PLATAFORMA", y = "SEGUIDORES", color="NOME", barmode="group", color_discrete_map=cores_personalizadas)
        grafico_seguidores.update_yaxes(tickformat=",.2s")
        grafico_idade = px.bar(df_idade, x = "IDADE", y = "SEGUIDORES IDADE", color="NOME", barmode="group", color_discrete_map=cores_personalizadas,
                               hover_data={'IDADE': True})
        grafico_idade.update_yaxes(tickformat=",.2s")
        grafico_genero = px.bar(df_genero, x = "GENERO", y = "SEGUIDORES GENERO", color="NOME", barmode="group", color_discrete_map=cores_personalizadas)
        grafico_genero.update_yaxes(tickformat=",.2s")
        grafico_autenticos = px.bar(df_autenticos, x = "NOME", y = "SEGUIDORES AUTÊNTICOS", color="NOME", color_discrete_map=cores_personalizadas)
        grafico_autenticos.update_xaxes(showticklabels=False)
        grafico_autenticos.update_yaxes(tickformat=",.2s")
        mapa = px.scatter_mapbox(df_mapa, lat = "LATITUDE", lon = "LONGITUDE", color = "NOME", size = "SEGUIDORES ESTADO", zoom = 10, opacity=0.6, 
                                hover_data={'ESTADO': True, "LATITUDE": False, "LONGITUDE": False}, color_discrete_map=cores_personalizadas)


        titulo_seguidores = "Quantidade de seguidores por plataforma"
        titulo_idade = "Quantidade total de seguidores por idade"
        titulo_genero = "Quantidade total de seguidores por gênero"
        titulo_autenticos = "Quantidade total de seguidores autênticos"
        titulo_mapa = "Quantidade total de seguidores por estado"




    # atualizando layout dos graficos
    grafico_seguidores.update_layout(margin=go.layout.Margin(l=5, r=5, t=30, b=0), template = tema, showlegend = False,
                                     title={"text": titulo_seguidores, 'y': 0.96, "x": 0.5}, xaxis_title="", yaxis_title=""), 
    grafico_idade.update_layout(margin=go.layout.Margin(l=5, r=5, t=30, b=0), template = tema, showlegend = False,
                                title={"text": titulo_idade, 'y': 0.96, "x": 0.2}, xaxis_title="", yaxis_title="")
    grafico_genero.update_layout(margin=go.layout.Margin(l=5, r=5, t=30, b=0), template = tema, showlegend = False,
                                 title={"text": titulo_genero, 'y': 0.96, "x": 0.1, "font": {"size": 15}}, xaxis_title="", yaxis_title="")
    grafico_autenticos.update_layout(margin=go.layout.Margin(l=5, r=5, t=30, b=10), template = tema, showlegend = False,
                                     title={"text": titulo_autenticos, 'y': 0.97, "x": 0.8}, xaxis_title="", yaxis_title="")
    mapa.update_layout(margin=go.layout.Margin(l=5, r=5, t=30, b=0), template = tema, showlegend = False,
                       mapbox = dict(center=go.layout.mapbox.Center(lat = lat_mean, lon = lon_mean)),
                       title={"text": titulo_mapa, 'y': 0.97, "x": 0.5})    
    

    # return
    return grafico_seguidores, grafico_genero, grafico_idade, grafico_autenticos, mapa

# PAGINA GERAL - ABA PERFORMANCE DE CONTEUDO
@app.callback(
        [
            Output("grafico-geral-total-posts", "figure"),
            Output("grafico-geral-vmg", "figure"),
            Output("grafico-geral-total-engajamento", "figure"),
            Output("grafico-geral-taxa-engajamento", "figure"),
        ],
        [
            Input('checklist-politicos-geral', 'value'),
            Input('radio-items-geral', 'value'),
        ]
)
def update_graficos_geral_pc(selected_values, operacao):


    df_posts = posts[(posts["Nome"].isin(selected_values)) & (posts["Plataforma"] == "Total")]
    data_inicial = df_posts["Data"].unique()[0]
    data_final = df_posts["Data"].unique()[-1]

    posts["Nome"].unique()

    if operacao == "percentual":

        df_posts = df_posts.pivot_table(index="Data", columns="Nome", values=["Total de Posts", "Engajamento Total", "Taxa de Engajamento", "VMG"]).pct_change(fill_method=None)
        df_posts.iloc[0, :] = 0
        df_posts = df_posts.reset_index().melt(id_vars=['Data'], var_name=['Métrica', 'Nome'], value_name='Valor').pivot_table(columns="Métrica", values="Valor", index=["Nome", "Data"]).reset_index()

        grafico_total_posts = px.line(df_posts, x = "Data", y="Total de Posts", color="Nome",color_discrete_map=cores_personalizadas)
        grafico_total_posts.update_yaxes(tickformat=",.1%")
        grafico_vmg = px.line(df_posts, x = "Data", y="VMG", color="Nome",color_discrete_map=cores_personalizadas)
        grafico_vmg.update_yaxes(tickformat=",.1%")
        grafico_total_engajamento = px.line(df_posts, x = "Data", y="Engajamento Total", color="Nome", color_discrete_map=cores_personalizadas)
        grafico_total_engajamento.update_yaxes(tickformat=",.1%")
        grafico_taxa_engajamento = px.line(df_posts, x = "Data", y="Taxa de Engajamento", color="Nome", color_discrete_map=cores_personalizadas)
        grafico_taxa_engajamento.update_yaxes(tickformat=",.1%")

        titulo_posts = f"Variação percentual (%) do total de posts entre {data_inicial} e {data_final}"
        titulo_vmg = f"Variação percentual (%) do VMG entre {data_inicial} e {data_final}"
        titulo_engajamento = f"Variação percentual (%) do total de engajamento entre {data_inicial} e {data_final}"
        ttiulo_taxa = f"Variação percentual (%) da taxa de engajamento entre {data_inicial} e {data_final}"

    else:

        grafico_total_posts = px.area(df_posts, x = "Data", y="Total de Posts", color="Nome",color_discrete_map=cores_personalizadas)
        grafico_vmg = px.area(df_posts, x = "Data", y="VMG", color="Nome",color_discrete_map=cores_personalizadas)
        grafico_vmg.update_yaxes(tickformat=",.2s")
        grafico_total_engajamento = px.area(df_posts, x = "Data", y="Engajamento Total", color="Nome", color_discrete_map=cores_personalizadas)
        grafico_total_engajamento.update_yaxes(tickformat=",.2s")
        grafico_taxa_engajamento = px.area(df_posts, x = "Data", y="Taxa de Engajamento", color="Nome", color_discrete_map=cores_personalizadas)
        grafico_taxa_engajamento.update_yaxes(tickformat=",.1%")

        titulo_posts = f"Variação do total de posts entre {data_inicial} e {data_final}"
        titulo_vmg = f"Variação do total de VMG {data_inicial} e {data_final}"
        titulo_engajamento = f"Variação do total de engajamento entre {data_inicial} e {data_final}"
        ttiulo_taxa = f"Variação da taxa de engajamento entre {data_inicial} e {data_final}"        

    grafico_total_posts.update_traces(mode="markers+lines", hovertemplate=None)
    grafico_total_posts.update_layout(margin=go.layout.Margin(l=5, r=5, t=30, b=0), template = tema, showlegend = False,
                                      title={"text": titulo_posts, 'y': 0.97, "x": 0.05, "font": {"size": 12}}, hovermode="x", xaxis_title="", yaxis_title="")
    grafico_vmg.update_traces(mode="markers+lines", hovertemplate=None)
    grafico_vmg.update_layout(margin=go.layout.Margin(l=5, r=5, t=30, b=0), template = tema, showlegend = False,
                                      title={"text": titulo_vmg, 'y': 0.97, "x": 0.05, "font": {"size": 12}}, hovermode="x", xaxis_title="", yaxis_title="")
    grafico_total_engajamento.update_traces(mode="markers+lines", hovertemplate=None)
    grafico_total_engajamento.update_layout(margin=go.layout.Margin(l=5, r=5, t=30, b=0), template = tema, showlegend = False,
                                            title={"text": titulo_engajamento, 'y': 0.97, "x": 0.05, "font": {"size": 12}}, hovermode="x", xaxis_title="", yaxis_title="")
    grafico_taxa_engajamento.update_traces(mode="markers+lines", hovertemplate=None)
    grafico_taxa_engajamento.update_layout(margin=go.layout.Margin(l=5, r=5, t=30, b=0), template = tema, showlegend = False,
                                           title={"text": ttiulo_taxa, 'y': 0.97, "x": 0.05, "font": {"size": 12}}, hovermode="x", xaxis_title="", yaxis_title="")

    return grafico_total_posts, grafico_vmg, grafico_total_engajamento, grafico_taxa_engajamento

# PAGINA INDIVIDUAL - ABA VISAO GERAL
@app.callback(
    [
        Output("grafico-seguidores-individual", "figure"),
        Output("grafico-idade-individual", "figure"),
        Output("grafico-genero-individual", "figure"),
        Output("grafico-mapa-individual", "figure"),
    ],
        Input('dropdown-politico', 'value'),
)
def update_graficos_visao_geral(selected_value):

    # datasets
    df_seguidores = seguidores[(seguidores["NOME"] == selected_value) & (seguidores["PLATAFORMA"] != "TOTAL")].reset_index(drop=True)
    df_seguidores["% SEGUIDORES"] = df_seguidores["SEGUIDORES"] / df_seguidores["SEGUIDORES"].sum()
    df_idade = idade[idade["NOME"] == selected_value]
    df_genero = genero[genero["NOME"] == selected_value]
    df_mapa = local[local["NOME"] == selected_value]
    estados_com_mais_seguidores = df_mapa.groupby("ESTADO")['% SEGUIDORES ESTADO'].sum().sort_values(ascending=False).head(10).index
    df_mapa = df_mapa[df_mapa["ESTADO"].isin(estados_com_mais_seguidores)]


    # lista com plataformas para auxiliar na criacao das cores
    plataformas = df_genero["PLATAFORMA"].unique().tolist()
    # criando cores personalizadas
    cores = px.colors.sequential.Viridis
    cores_personalizadas = {}
    for i in range(len(plataformas)):
        cores_personalizadas[plataformas[i]] = cores[i+1]

    # grafico seguidores
    grafico_seguidores = px.bar(df_seguidores, y = "PLATAFORMA", x = "SEGUIDORES", color="PLATAFORMA", color_discrete_map=cores_personalizadas)
    grafico_seguidores.update_yaxes(showticklabels=False)  
    # grafico de idade
    grafico_idade = px.bar(df_idade, x = "IDADE", y = "% SEGUIDORES IDADE", color = "PLATAFORMA", barmode="group", color_discrete_map=cores_personalizadas)
    grafico_idade.update_yaxes(tickformat=".1%")

    # grafico de genero
    grafico_genero = go.Figure()
    # intervalos dos valores para plotagem no eixo x
    intervalos = [
        [0.05, 0.2],
        [0.3, 0.45],
        [0.55, 0.7],
        [0.8, 0.95],
    ]
    # criando grafico de pizza para cada plataforma
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
            domain=dict(x=intervalos[idx], y=[0, 1]),
            marker=dict(colors=colors),
            showlegend=False
        ))
    # setando nome no eixo x
    eixo_x = [
        {'text': 'INSTAGRAM', 'x': 0.04, 'y': 0.05, 'font_size': 20, 'showarrow': False},
        {'text': 'X', 'x': 0.375, 'y': 0.05, 'font_size': 20, 'showarrow': False},
        {'text': 'TIKTOK', 'x': 0.62, 'y': 0.05, 'font_size': 20, 'showarrow': False},
        {'text': 'YOUTUBE', 'x': 0.94, 'y': 0.05, 'font_size': 20, 'showarrow': False}
        ]

    # grafico de mapas
    grafico_mapa = px.bar(df_mapa, x="% SEGUIDORES ESTADO", y="ESTADO", color="PLATAFORMA", barmode="group", color_discrete_map=cores_personalizadas)
    grafico_mapa.update_xaxes(tickformat=".1%")
    
    
    # atualizando layout dos graficos
    grafico_seguidores.update_layout(margin=go.layout.Margin(l=5, r=5, t=35, b=0), template = tema, showlegend = True,
                                title={"text": "Quantidade total de seguidores por plataforma", 'y': 0.95, "x": 0.025}, xaxis_title="", yaxis_title="")
    grafico_idade.update_layout(margin=go.layout.Margin(l=5, r=5, t=35, b=0), template = tema, showlegend = False,
                                title={"text": "Distribuição (%) dos seguidores por idade e plataforma", 'y': 0.95, "x": 0.5}, xaxis_title="", yaxis_title="")
    grafico_genero.update_layout(margin=go.layout.Margin(l=5, r=5, t=5, b=0), template = tema, showlegend = False,
                                 title={"text": "Distribuição (%) dos seguidores por gênero e plataforma", 'y': 0.9})
    grafico_mapa.update_layout(margin=go.layout.Margin(l=5, r=5, t=35, b=0), template = tema, showlegend = False,
                               title={"text": "Distribuição (%) dos seguidores por gênero e plataforma", 'y': 0.96}, xaxis_title="", yaxis_title="")

    return grafico_seguidores, grafico_idade, grafico_genero, grafico_mapa

# PAGINA INDIVIDUAL - ABA PERFORMANCE DE CONTEUDO - GRAFICOS COMPLETO
@app.callback(
        [
            Output("grafico-total-posts-final", "figure"),
            Output("grafico-engajamento-total-final", "figure"),
            Output("grafico-engajamento-taxa-final", "figure"),
            Output("grafico-vmg-final", "figure"),
        ],
        [
            Input('dropdown-politico', 'value'),
            # Input('accordion-conteudo', 'active_item'),
        ]
)
def update_graficos_conteudo_final(selected_value):

    df_conteudo = conteudo[conteudo["Nome"] == selected_value]
    df_total_posts = df_conteudo.groupby(["Nome", "Semana", "Plataforma"], observed=True).size().reset_index(name="Total de Posts")
    df_engajamento_total = df_conteudo.groupby(["Nome", "Semana", "Plataforma"], observed=True)[["Engajamento"]].sum().reset_index()
    df_engajamento_taxa = df_conteudo.groupby(["Nome", "Semana", "Plataforma"], observed=True)[["Taxa de Engajamento"]].mean().reset_index()
    df_vmg = df_conteudo.groupby(["Nome", "Semana", "Plataforma"], observed=True)[["VMG"]].sum().reset_index()

    # lista com plataformas para auxiliar na criacao das cores
    plataformas = df_conteudo["Plataforma"].unique().tolist()
    # criando cores personalizadas
    cores = px.colors.sequential.Viridis
    cores_personalizadas = {}
    for i in range(len(plataformas)):
        cores_personalizadas[plataformas[i]] = cores[i+1]

    grafico_total_posts = px.bar(df_total_posts, x = "Semana", y = "Total de Posts", color = "Plataforma", barmode="group", color_discrete_map=cores_personalizadas)
    grafico_total_engajamento = px.bar(df_engajamento_total, x = "Semana", y = "Engajamento", color = "Plataforma", barmode="group", color_discrete_map=cores_personalizadas)
    grafico_taxa_engajamento = px.bar(df_engajamento_taxa, x = "Semana", y = "Taxa de Engajamento", color = "Plataforma", barmode="group", color_discrete_map=cores_personalizadas)
    grafico_taxa_engajamento.update_yaxes(tickformat=".1%")
    grafico_vmg = px.bar(df_vmg, x = "Semana", y = "VMG", color = "Plataforma", barmode="group", color_discrete_map=cores_personalizadas)    

    grafico_total_posts.update_layout(margin=go.layout.Margin(l=5, r=5, t=35, b=0), template = tema, showlegend = True,
                                title={"text": "Quantidade total de posts por plataforma", 'y': 0.95, "x": 0.025}, xaxis_title="", yaxis_title="")
    grafico_total_engajamento.update_layout(margin=go.layout.Margin(l=5, r=5, t=35, b=0), template = tema, showlegend = True,
                                title={"text": "Quantidade total de engajamento por plataforma", 'y': 0.95, "x": 0.025}, xaxis_title="", yaxis_title="")
    grafico_taxa_engajamento.update_layout(margin=go.layout.Margin(l=5, r=5, t=35, b=0), template = tema, showlegend = True,
                                title={"text": "Taxa de engajamento médio por plataforma", 'y': 0.95, "x": 0.025}, xaxis_title="", yaxis_title="")
    grafico_vmg.update_layout(margin=go.layout.Margin(l=5, r=5, t=35, b=0), template = tema, showlegend = True,
                                title={"text": "Quantidade total de VMG por plataforma", 'y': 0.95, "x": 0.025}, xaxis_title="", yaxis_title="")
    

    return grafico_total_posts, grafico_total_engajamento, grafico_taxa_engajamento, grafico_vmg

# PAGINA INDIVIDUAL - ABA PERFORMANCE DE CONTEUDO - GRAFICOS SEMANAIS
@app.callback(
        [
            Output("graficos-semana1", "children"),
            Output("graficos-semana2", "children"),
            Output("graficos-semana3", "children"),
        ],
        [
            Input("dropdown-politico", "value"),
            Input("accordion-conteudo", "active_item"),
        ],
)
def update_graficos_conteudo_semanal(selected_value, item_ativo):

    # selected_value = "Abilio Brunini"

    plataformas = posts["Plataforma"].unique().tolist()
    # criando cores personalizadas
    cores = px.colors.sequential.Viridis
    cores_personalizadas = {}
    for i in range(len(plataformas)):
        cores_personalizadas[plataformas[i]] = cores[i+1]    

    df_posts = conteudo[conteudo["Nome"] == selected_value]

    if item_ativo == "post-semana1":

        df_posts = df_posts[df_posts["Semana"] == "14-20 MAR/24"]
        fig1, fig2, fig3, fig4, caixas = funcs.criar_graficos_semanal(df_posts)
        elemento = funcs.layout_graficos_semanal(fig1, fig2, fig3, fig4, caixas)

        return [elemento, "", ""]
    
    elif item_ativo == "post-semana2":
        
        df_posts = df_posts[df_posts["Semana"] == "4-10 SET/24"]
        fig1, fig2, fig3, fig4, caixas = funcs.criar_graficos_semanal(df_posts)
        elemento = funcs.layout_graficos_semanal(fig1, fig2, fig3, fig4, caixas)

        return ["", elemento, ""]
    
    elif item_ativo == "post-semana3":

        df_posts = df_posts[df_posts["Semana"] == "12-18 JUN/24"]
        fig1, fig2, fig3, fig4, caixas = funcs.criar_graficos_semanal(df_posts)
        elemento = funcs.layout_graficos_semanal(fig1, fig2, fig3, fig4, caixas)        

        return ["", "", elemento]
    
    else:

        return ["", "", ""]

# PAGINA INDIVIDUAL - ABA PERFORMANCE DE CONTEUDO - POSTS SEMANAIS
@app.callback(
        [
            Output("top-posts-semana1", "children"),
            Output("top-posts-semana2", "children"),
            Output("top-posts-semana3", "children"),
        ],
        [
            Input("dropdown-politico", "value"),
            Input("accordion-conteudo", "active_item")
        ]
)
def update_posts_cards(selected_value, item_ativo):

    # selected_value = "Abilio Brunini"

    df_top_posts = top_posts[(top_posts["Nome"] == selected_value)] 

    if item_ativo == "post-semana1":

        df_top_posts1 = df_top_posts[df_top_posts["Semana"] == "14-20 MAR/24"].reset_index(drop=True)
        elemento = funcs.layout_cards_semanais(df_top_posts1, 1)

        return [elemento, "", ""]

    elif item_ativo == "post-semana2":

        df_top_posts2 = df_top_posts[df_top_posts["Semana"] == "4-10 SET/24"].reset_index(drop=True)
        elemento = funcs.layout_cards_semanais(df_top_posts2, 2)

        return ["", elemento, ""]
    
    elif item_ativo == "post-semana3":

        df_top_posts3 = df_top_posts[df_top_posts["Semana"] == "12-18 JUN/24"].reset_index(drop=True)
        elemento = funcs.layout_cards_semanais(df_top_posts3, 3)        

        return ["", "", elemento]
    
    else:

        return ["", "", ""]

# PAGINA INDIVIDUAL - ABA PERFORMANCE DE CONTEUDO - POSTS SEMANAIS
@app.callback(
        [
            Output("div-mostrar-posts", "hidden"),
            Output("top-posts-semana1", "hidden", allow_duplicate=True),
            Output("graficos-semana1", "hidden"),
            Output("top-posts-semana2", "hidden", allow_duplicate=True),
            Output("graficos-semana2", "hidden"),
            Output("top-posts-semana3", "hidden", allow_duplicate=True),
            Output("graficos-semana3", "hidden"),
        ],
        [
            Input("accordion-conteudo", "active_item"),
            Input("mostrar-posts", "value"),
        ],
        prevent_initial_call=True,
)
def mostrar_posts(item_ativo, valor):


    if item_ativo == "post-semana1":

        if valor == "Gráficos":

            return [False, 
                    True, False, # semana 1
                    True, True, # semana 2
                    True, True # semana 3
                    ] 
        
        else:
            
            return [False, False, True, True, True, True, True]

    if item_ativo == "post-semana2":

        if valor == "Gráficos":

            return [False, True, True, True, False, True, True]
        
        else:
            
            return [False, True, True, False, True, True, True]

    if item_ativo == "post-semana3":

        if valor == "Gráficos":

            return [False, True, True, True, True, True, False]
        
        else:
            
            return [False, True, True, True, True, False, True]
        
    else:
            
        return [True, True, True, True, True, True, True]

# ESCONDER RADIO POST GRAFICO NO PERFIL INDIVIDUAL GERAL
@app.callback(
        [
            Output("div-mostrar-posts", "hidden", allow_duplicate=True),
        ], 
        [
            Input("tabs", "active_tab")
        ],
        prevent_initial_call=True
        )
def esconder_radio_posts_graficos(at):

    if at == "tab-geral":

        return [True]
    else:

        return [False]

# CRIA O GRAFICO DE CONEXOES
@app.callback(
        [
            Output("grafico-conexoes-individual", "elements"),
            Output("grafico-conexoes-individual", "stylesheet"),
        ],
        [
            Input('dropdown-politico', 'value'),
            Input('accordion-individual', 'active_item'),
        ],
        prevent_initial_call=True
)
def updtate_conexoes(selected_value, ativo):

    elementos = conexao[selected_value]

    if ativo == "conexao-accordion":
        return elementos, conexao_stylesheet
    else:
        return elementos, conexao_stylesheet 

# ADICIONA INTERATIVIDADE AS CONEXOES
@app.callback(
    [
        Output('grafico-conexoes-individual', 'stylesheet', allow_duplicate=True),
        Output("conexao-selecionada", "children"),
        Output("metrica-conexao-selecionada", "children"),
        Output("engajamento-conexao-selecionada", "children"),
        Output("posts-conexao-selecionada", "children"),
        Output("link-conexao-selecionada", "href"),
        Output("link-conexao-selecionada", "color"),
    ],
    [
        Input('grafico-conexoes-individual', 'tapNode'),
        Input('grafico-conexoes-individual', 'selectedNodeData'),
        Input("dropdown-politico", "value")
    ],
    prevent_initial_call=True
)
def generate_stylesheet(node, data_list, selected_value):

    if not data_list:
        return conexao_stylesheet, "", "", "", "", "", ""


    elif node:
        node_id = node['data']['id']
    
        stylesheet = [{
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
                'opacity': 0.3,
                'text-wrap': 'wrap',
                'text-max-width': 80,
                'font-weight': 'bold',
            }
        }, {
            'selector': 'edge',
            'style': {
                "line-fill": "linear-gradient",
                'width': 0.1,
                'curve-style': 'haystack',
                'source-endpoint': 'outside-to-node',
                'target-endpoint': 'outside-to-node',
                'opacity': 0.1,
                # 'control-point-step-size': 3
            }
        },{
            "selector": 'node[id = "{}"]'.format(node_id),
            "style": {
                'label': 'data(label)',
                'background-color': 'data(color)',
                'text-valign': 'center',
                'text-halign': 'center',
                'border-width': 1.5,
                "border-opacity": 1,
                'width': 'data(size)',
                'height': 'data(size)',
                'opacity': 0.98,
                'z-index': 9999,
            }
        },{
            "selector": 'node[id = "0"]',
            "style": {
                'label': 'data(label)',
                'background-color': 'data(color)',
                'text-valign': 'center',
                'text-halign': 'center',
                'border-width': 1.5,
                "border-opacity": 1,
                'width': 'data(size)',
                'height': 'data(size)',
                'opacity': 0.8,
                'z-index': 9999,
            }
        }
        ]

        for edge in node["edgesData"]:
            
            if edge["target"] == node_id:

                stylesheet.append(
                    {
                        "selector": 'edge[id= "{}"]'.format(edge['id']),
                        "style": {
                            'width': 1,
                            'curve-style': 'bezier',
                            'source-endpoint': 'outside-to-node',
                            'target-endpoint': 'outside-to-node',
                            'control-point-step-size': 5,
                            'opacity': 0.9,
                            'z-index': 5000,
                            'label': 'data(pct)',
                            'text-valign': 'center',
                            'text-halign': 'center',
                            'color': 'rgb(255, 255, 255)',                                           
                        }                        
                    }                   
                )        
        
        
        
        
        nome = node['data']['label_selected']

        if nome == selected_value:
            return conexao_stylesheet, "", "", "", "", "", ""

        metrica = df_conexao.loc[(df_conexao['Nome'] == selected_value) & (df_conexao["Conexão"] == nome), "Metrica"].values[0]
        engajamento = df_conexao.loc[(df_conexao['Nome'] == selected_value) & (df_conexao["Conexão"] == nome), "Engajamento"].values[0]
        posts = df_conexao.loc[(df_conexao['Nome'] == selected_value) & (df_conexao["Conexão"] == nome), "Total de Posts"].values[0]
        link = df_conexao.loc[(df_conexao['Nome'] == selected_value) & (df_conexao["Conexão"] == nome), "Top Post"].values[0]

        return stylesheet, nome, f"{metrica:,.0f}".replace(",", "."), f"{engajamento:,.0f}".replace(",", "."), posts, link, "primary"

# TOAST INFORMACOES CONEXOES
@app.callback(
    Output("conexoes-toast", "is_open"),
    [
        Input("conexoes-button-toast", "n_clicks"),
        Input("conexoes-toast", "is_open"),
    ],
)
def open_toast(n, aberto):

    if aberto:
        inicio = time.time()    
        tempo_decorrido = time.time() - inicio
        if n:
            return False
        else:
            return True
    else:

        if n:
            return True
        else:
            return False

# TOOLTIPS PARA POSTS SEMANAIS
@app.callback(
        [
            Output("tooltips-semana1", "children"),
            Output("tooltips-semana2", "children"),
            Output("tooltips-semana3", "children"),
        ],
            Input("accordion-conteudo", "active_item")    
)
def generate_tooltips(active_item):

    if active_item == "post-semana1":

        retorno = [funcs.criar_tooltips(semana=1), "", ""]

    elif active_item == "post-semana2":

        retorno = ["", funcs.criar_tooltips(semana=2), ""]

    elif active_item == "post-semana3":

        retorno = ["", "", funcs.criar_tooltips(semana=3)]
    
    else:

        retorno = ["", "", ""]


    return retorno



# =================================== #
# RUN SERVER
# =================================== #

if __name__ == "__main__":
    app.run(debug=True)





























