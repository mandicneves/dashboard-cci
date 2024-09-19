import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Output
from dash import html, dcc


def formatar_numero(numero):
    if abs(numero) >= 1_000_000:
        return f"{numero / 1_000_000:.2f}M"
    elif abs(numero) >= 1_000:
        return f"{numero / 1_000:.2f}K"
    return str(numero)

def gerar_cores(n):
    # Paleta de cores categóricas disponíveis no Plotly
    cores_disponiveis = px.colors.qualitative.Antique # Você pode escolher outras paletas como 'D3', 'G10', 'Bold', etc.

    # Replicando a paleta até alcançar o tamanho n
    cores = (cores_disponiveis * ((n // len(cores_disponiveis)) + 1))[:n]
    
    return cores

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

def criar_post_cards(df):

    posts_cards = []

    for idx, linha in df.iterrows():

        legenda = linha["Legenda"]
        likes = formatar_numero(int(linha["Likes"]))
        comentarios = formatar_numero(int(linha["Comentarios"]))
        impressoes = formatar_numero(int(linha["Impressoes"]))
        views = formatar_numero(int(linha["Visualizacoes"]))
        engajamento = formatar_numero(int(linha["Engajamento"]))
        compartilhamentos = formatar_numero(int(linha["Compartilhamentos"]))
        link = linha["Link"] 

        card = html.Div(
            dbc.Container(
                [
                    html.H1(f"Post-0{idx+1}", className="display-6"),
                    html.P(legenda, className="lead", 
                           style={"font-size": "1vw", 
                                  "width": "200px", 
                                  "height": "80px", 
                                  "overflow": "hidden"}),
                    html.Hr(className="my-2"),
                    dbc.Row([
                        dbc.Col(f"❤️ {likes}", id=f"likes-{idx+1}", style={"margin-left": "15px", "font-size": "1.1vw"}),
                        dbc.Col(f"💬 {comentarios}", id=f"comentarios-{idx+1}", style={"margin-right": "15px", "font-size": "1.1vw"}),
                    ], style={"margin-top": "10px"}),
                    dbc.Row([
                        dbc.Col(f"💭 {impressoes}", id=f"impressoes-{idx+1}", style={"margin-left": "15px", "font-size": "1.1vw"}),
                        dbc.Col(f"📈 {views}", id=f"views-{idx+1}", style={"margin-right": "15px", "font-size": "1.1vw"}),
                    ], style={"margin-top": "10px"}),
                    dbc.Row([
                        dbc.Col(f"👍 {engajamento}", id=f"engajamento-{idx+1}", style={"margin-left": "15px", "font-size": "1.1vw"}),
                        dbc.Col(f"🔄 {compartilhamentos}", id=f"compartilhamentos-{idx+1}", style={"margin-right": "15px", "font-size": "1.1vw"}),
                    ], style={"margin-top": "10px", "margin-bottom": "10px"}),
                    html.Hr(className="my-2"),
                    html.P(dbc.Button("Link", color="primary", outline=True, href=link, style={"margin-top": "15px"}), className="d-grid gap-2"),
                ],
                fluid=True,
                className="py-3", style={"height": "45vh"}
            ),
            className="p-3 bg-body-secondary rounded-3",
        )    

        posts_cards.append(card)


    return posts_cards

def criar_tooltips(df):

    tooltips = []

    for i in range(len(df)):

        likes = dbc.Tooltip("Likes", target=f"likes-{i+1}", placement="top")
        comentarios = dbc.Tooltip("Comentarios", target=f"comentarios-{i+1}", placement="top")
        impressoes = dbc.Tooltip("Impressões", target=f"impressoes-{i+1}", placement="top")
        visualizacoes = dbc.Tooltip("Visualizações", target=f"views-{i+1}", placement="top")
        engajamento = dbc.Tooltip("Engajamento", target=f"engajamento-{i+1}", placement="top")
        compartilhamentos = dbc.Tooltip("Compartilhamentos", target=f"compartilhamentos-{i+1}", placement="top")
        
        tooltips.append(likes)
        tooltips.append(comentarios)
        tooltips.append(impressoes)
        tooltips.append(visualizacoes)
        tooltips.append(engajamento)
        tooltips.append(compartilhamentos)

    return tooltips

def layout_cards_semanais(df):

    try:
        card1, card2, card3 = criar_post_cards(df)
        elemento = html.Div([
            dbc.Row([
                dbc.Col([card1], sm=3, width={"offset": 1}),
                dbc.Col([card2], sm=3, style={"margin-left": "20px", "margin-right": "20px"}),
                dbc.Col([card3], sm=3),
            ]),
            html.Div(criar_tooltips(df))
        ])
    except:
        # elemento = ""
        card1, card2 = criar_post_cards(df)
        elemento = html.Div([
            dbc.Row([
                dbc.Col([card1], sm=3, width={"offset": 2}),
                dbc.Col([card2], sm=3, style={"margin-left": "20px", "margin-right": "20px"}),
            ]),
            html.Div(criar_tooltips())
        ])

    return elemento