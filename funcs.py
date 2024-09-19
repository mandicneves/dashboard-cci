import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Output
from dash import html, dcc

def gerar_cores(n):
    # Paleta de cores categóricas disponíveis no Plotly
    cores_disponiveis = px.colors.qualitative.Antique # Você pode escolher outras paletas como 'D3', 'G10', 'Bold', etc.

    # Replicando a paleta até alcançar o tamanho n
    cores = (cores_disponiveis * ((n // len(cores_disponiveis)) + 1))[:n]
    
    return cores

# Função para criar a lista de opções com os círculos coloridos
def criar_opcoes(dados, cores_personalizadas):
    opcoes = [{"label": "Todos", "value": "Todos"}]
    for nome in dados["NOME"].unique():
        cor = cores_personalizadas.get(nome, 'rgb(0, 0, 0)')  # Cor preta como fallback
        opcoes.append({
            'label': html.Span([
                nome,  # Nome do político
                html.Span(  # Círculo colorido
                    style={
                        'display': 'inline-block',
                        'width': '12px',
                        'height': '12px',
                        'border-radius': '50%',
                        'background-color': cor,
                        'margin-left': '10px'
                    }
                )
            ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),
            'value': nome
        })
    return opcoes

def ajustar_intensidade(cor, fator):
    """Retorna a cor ajustada, clareando ou escurecendo de acordo com o fator"""
    cor = cor.lstrip('#')
    rgb = tuple(int(cor[i:i+2], 16) for i in (0, 2, 4))
    ajustado = tuple(min(255, int(c * fator)) for c in rgb)
    return '#{:02x}{:02x}{:02x}'.format(*ajustado)

def criar_graficos_semanal(df_posts):

    tema = "cyborg"

    plataformas = df_posts["Plataforma"].unique().tolist()
    # criando cores personalizadas
    cores = px.colors.sequential.Viridis
    cores_personalizadas = {}
    for i in range(len(plataformas)):
        cores_personalizadas[plataformas[i]] = cores[i+1]       

    df_total_posts = df_posts.groupby(["Data", "Plataforma"]).size().reset_index(name="Total de Posts")
    df_total_engajamento = df_posts.groupby(["Data", "Plataforma"])["Engajamento"].sum().reset_index()
    df_taxa_engajamento = df_posts.groupby(["Data", "Plataforma"])["Taxa de Engajamento"].mean().reset_index()
    df_vmg = df_posts.groupby(["Data", "Plataforma"])["VMG"].sum().reset_index()
    

    grafico_total_posts = px.bar(df_total_posts, x = "Data", y = "Total de Posts", color = "Plataforma", barmode="group", color_discrete_map=cores_personalizadas)
    grafico_total_engajamento = px.bar(df_total_engajamento, x = "Data", y = "Engajamento", color = "Plataforma", barmode="group", color_discrete_map=cores_personalizadas)
    grafico_taxa_engajamento = px.bar(df_taxa_engajamento, x = "Data", y = "Taxa de Engajamento", color = "Plataforma", barmode="group", color_discrete_map=cores_personalizadas)
    grafico_taxa_engajamento.update_yaxes(tickformat=".1%")
    grafico_vmg = px.bar(df_vmg, x = "Data", y = "VMG", color = "Plataforma", barmode="group", color_discrete_map=cores_personalizadas)


    grafico_total_posts.update_layout(margin=go.layout.Margin(l=5, r=5, t=35, b=0), template = tema, showlegend = False,
                                title={"text": "Quantidade total de posts por plataforma", 'y': 0.95, "x": 0.025})
    grafico_total_engajamento.update_layout(margin=go.layout.Margin(l=5, r=5, t=35, b=0), template = tema, showlegend = False,
                                title={"text": "Quantidade total de engajamento por plataforma", 'y': 0.95, "x": 0.025})
    grafico_taxa_engajamento.update_layout(margin=go.layout.Margin(l=5, r=5, t=35, b=0), template = tema, showlegend = False,
                                title={"text": "Taxa de engajamento médio por plataforma", 'y': 0.95, "x": 0.025})
    grafico_vmg.update_layout(margin=go.layout.Margin(l=5, r=5, t=35, b=0), template = tema, showlegend = False,
                                title={"text": "Quantidade total de VMG por plataforma", 'y': 0.95, "x": 0.025})

    return grafico_total_posts, grafico_total_engajamento, grafico_taxa_engajamento, grafico_vmg

def layout_graficos_semanal(fig1, fig2, fig3, fig4):
                
    elemento = html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Graph(id = "grafico-total-posts-semana1", figure=fig1, style={"height": "30vh", "margin-right": "10px"}),
            ], sm=6),
            dbc.Col([
                dcc.Graph(id = "grafico-engajamento-total-semana1", figure=fig2, style={"height": "30vh"}),
            ], sm=6),
    ], className="g-0"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "grafico-engajamento-taxa-semana1", figure=fig3, style={"height": "30vh", "margin-right": "10px", "margin-top": "10px"}),
        ], sm=6),
        dbc.Col([
            dcc.Graph(id = "grafico-vmg-semana1", figure=fig4, style={"height": "30vh", "margin-top": "10px"}),
        ], sm=6),
    ], className="g-0"),
    ])

    return elemento

def make_postcard_output():

    outs = []

    for i in range(1, 4):

        aux = []

        likes = Output(f"likes-{i}", "value")
        comentarios = Output(f"comentarios-{i}", "value")
        impressoes = Output(f"impressoes-{i}", "value")
        liftconteudo = Output(f"lift-conteudo-{i}", "value")
        taxaengajamento = Output(f"taxa-engajamento-{i}", "value")
        compartilhamentos = Output(f"compartilhamentos-{i}", "value")

        aux.append(likes)
        aux.append(comentarios)
        aux.append(impressoes)
        aux.append(liftconteudo)
        aux.append(taxaengajamento)
        aux.append(compartilhamentos)

        outs.extend(aux)
    
    return outs

def make_postcard(i, likes, comentarios, impressoes, views, engajamento, compartilhamento, link):

    post_card = dbc.Card(
        [
            # dbc.CardImg(src="", top=True, style={"height": "40%"}),  # Substitua pelo caminho da sua imagem
            dbc.CardBody(
                [
                    # Primeira linha
                    dbc.Row(
                        [
                            dbc.Col(html.Div(f"❤️ {likes}"), width=6),  # Emoji de coração
                            dbc.Col(html.Div(f"💬 {comentarios}"), width=6),  # Emoji de comentário
                        ],
                        # className="mb-2",
                    ),
                    # Segunda linha
                    dbc.Row(
                        [
                            dbc.Col(html.Div(f"💭 {impressoes}"), width=6),  # Emoji de balão de pensamento
                            dbc.Col(html.Div(f"📈 {views}"), width=6),  # Emoji de gráfico de linha ascendente
                        ],
                        # className="mb-2",
                    ),
                    # Terceira linha
                    dbc.Row(
                        [
                            dbc.Col(html.Div(f"👍 {engajamento}"), width=6),  # Emoji de dedo polegar
                            dbc.Col(html.Div(f"🔄 {compartilhamento}"), width=6),  # Emoji de seta de compartilhamento
                        ],
                        # className="mb-2"
                    ),
                    html.Div([
                        # Botão no final do card
                        dbc.Button(
                            "Post", color="primary", outline=True, href=link
                        ),                    
                    ], className="d-grid gap-2", style={"margin-top": "20px"})

                ]
            ),
        ],
        style={
            "height": "20vh",  # Ajuste a altura do card
        },
    )


    return post_card