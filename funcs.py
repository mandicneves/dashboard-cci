import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import html, dcc



def formatar_numero(numero):
    if abs(numero) >= 1_000_000:
        return f"{numero / 1_000_000:.2f}M"
    elif abs(numero) >= 1_000:
        return f"{numero / 1_000:.2f}K"
    elif abs(numero) == 0:
        return ""
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
        if nome == 'Antonio Carlos Rodrigues':
            label = ["Antonio Carlos"]
        else:
            label = nome[:17] if len(nome) <= 17 else nome.split()[0],

        opcoes.append({
            'label': html.Span([
                label[0],  # Nome do político
                html.Span(  # Círculo colorido
                    style={
                        'display': 'inline-block',
                        'width': '20px',
                        'height': '15px',
                        'border-radius': '10%',
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

    tema = "minty"

    # plataformas = df_posts["Plataforma"].unique().tolist()
    # criando cores personalizadas
    # cores = px.colors.sequential.Viridis
    # cores_personalizadas = {}
    # for i in range(len(plataformas)):
    #     cores_personalizadas[plataformas[i]] = cores[i+1]

    cores_personalizadas = {"Instagram": "#80529e", "Twitter": "#1DA1F2", "TikTok": "#d1c39b", "YouTube": "#ad0202"}       

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
                                title={"text": "Quantidade total de posts por plataforma", 'y': 0.95, "x": 0.025}, xaxis_title="", yaxis_title="")
    grafico_total_engajamento.update_layout(margin=go.layout.Margin(l=5, r=5, t=35, b=0), template = tema, showlegend = True,
                                title={"text": "Quantidade total de engajamento por plataforma", 'y': 0.95, "x": 0.025}, xaxis_title="", yaxis_title="")
    grafico_taxa_engajamento.update_layout(margin=go.layout.Margin(l=5, r=5, t=35, b=0), template = tema, showlegend = True,
                                title={"text": "Taxa média de engajamento por plataforma", 'y': 0.95, "x": 0.025}, xaxis_title="", yaxis_title="")
    grafico_vmg.update_layout(margin=go.layout.Margin(l=5, r=5, t=35, b=0), template = tema, showlegend = True,
                                title={"text": "Quantidade total de VMG por plataforma", 'y': 0.95, "x": 0.025}, xaxis_title="", yaxis_title="")
    
    try:
        posts_insta = df_total_posts.loc[df_total_posts["Plataforma"] == "Instagram", "Total de Posts"].sum()
    except:
        posts_insta = 0
    try:
        posts_tiktok = df_total_posts.loc[df_total_posts["Plataforma"] == "TikTok", "Total de Posts"].sum()
    except:
        posts_tiktok = 0
    try:
        posts_x = df_total_posts.loc[df_total_posts["Plataforma"] == "Twitter", "Total de Posts"].sum()
    except:
        posts_x = 0
    try:
        posts_youtube = df_total_posts.loc[df_total_posts["Plataforma"] == "YouTube", "Total de Posts"].sum()
    except:
        posts_youtube = 0
    

    
    caixas = dbc.Container(
        dbc.Row(
            [
                html.H6("Contagem de Posts", style={"margin-bottom": "5px"}),
                # INSTAGRAM
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div([
                                    html.I(className="bi bi-instagram", style={"font-size": "12px", "color": "#E1306C"}),  # Ícone do Instagram
                                    html.P("Instagram", className="mb-0"),
                                    html.H6(f"{posts_insta}", className="mb-0"),
                                ], style={"text-align": "center"})
                            ]
                        ),
                        style={"width": "100%", "text-align": "center"}
                    ),
                ),
                # TWITTER
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div([
                                    html.I(className="bi bi-twitter", style={"font-size": "12px", "color": "#1DA1F2"}),  # Ícone do Twitter
                                    html.P("Twitter", className="mb-0"),
                                    html.H6(f"{posts_x}", className="mb-0"),
                                ], style={"text-align": "center"})
                            ]
                        ),
                        style={"width": "100%", "text-align": "center"}
                    ),
                ),
                # YOUTUBE
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div([
                                    html.I(className="bi bi-youtube", style={"font-size": "12px", "color": "#FF0000"}),  # Ícone do YouTube
                                    html.P("YouTube", className="mb-0"),
                                    html.H6(f"{posts_youtube}", className="mb-0"),
                                ], style={"text-align": "center"})
                            ]
                        ),
                        style={"width": "100%", "text-align": "center"}
                    ),
                ),
                # TIKTOK
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div([
                                    html.I(className="bi bi-tiktok", style={"font-size": "12px", "color": "#000000"}),  # Ícone do TikTok
                                    html.P("TikTok", className="mb-0"),
                                    html.H6(f"{posts_tiktok}", className="mb-0"),
                                ], style={"text-align": "center"})
                            ]
                        ),
                        style={"width": "100%", "text-align": "center"}
                    ),
                ),
            ],
            className="g-2",  # Gap entre as colunas
            style={"justify-content": "center", "margin-bottom": "10px", "margin-right": "8px"}  # Centralizar os elementos
        ),
        fluid=True
    ) 

    return grafico_total_posts, grafico_total_engajamento, grafico_taxa_engajamento, grafico_vmg, caixas

def criar_popover_grafico_semanal(semana):
    
    elemento = html.Div([        
        dbc.Popover(
            [
                dbc.PopoverHeader("Total de Posts", style={"background-color": "#78c2ad"}),
                dbc.PopoverBody("Soma das postagens realizadas no período."),
            ],
            target=f"grafico-total-posts-semana{semana}", trigger="click", id=f"dica-total-posts-semana{semana}"),
        dbc.Popover(
            [
                dbc.PopoverHeader("Total de Engajamento", style={"background-color": "#78c2ad"}),
                dbc.PopoverBody("Engajamento é o número de vezes que o público engajou com a publicação curtindo, comentando ou compartilhando."),
            ],
            target=f"grafico-engajamento-total-semana{semana}", trigger="click", id=f"dica-total-engajamento-semana{semana}"),
        dbc.Popover(
            [
                dbc.PopoverHeader("Taxa de Engajamento", style={"background-color": "#78c2ad"}),
                dbc.PopoverBody("Taxa de engajamento é o percentual do público que engajou com a publicação curtindo, comentando ou compartilhando."),
            ],
            target=f"grafico-engajamento-taxa-semana{semana}", trigger="click", id=f"dica-taxa-engajamento-semana{semana}"),
        dbc.Popover(
            [
                dbc.PopoverHeader("Total de VMG", style={"background-color": "#78c2ad"}),
                dbc.PopoverBody("VMG (Valor de Mídia Ganho) é um valor monetário estimado da publicação com base no tamanho do público alcançado."),
            ],
            target=f"grafico-vmg-semana{semana}", trigger="click", id=f"dica-vmg{semana}"),            

    ])

    return elemento

def layout_graficos_semanal(semana, fig1, fig2, fig3, fig4, caixas):
                
    elemento = html.Div([
        dbc.Row([
            dbc.Col([
                caixas,
                dcc.Graph(id = f"grafico-total-posts-semana{semana}", figure=fig1, style={"height": "20vh", "margin-right": "10px"},
                        config = {'toImageButtonOptions': {'format': 'png', 'filename': 'grafico-total-posts', 'height': 1080, 'width': 1920, 'scale': 1}}),
            ], sm=6),
            dbc.Col([
                dcc.Graph(id = f"grafico-engajamento-total-semana{semana}", figure=fig2, style={"height": "36.5vh"},
                        config = {'toImageButtonOptions': {'format': 'png', 'filename': 'grafico-total-engajamento', 'height': 1080, 'width': 1920, 'scale': 1}}),
            ], sm=6),
    ], className="g-0"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = f"grafico-engajamento-taxa-semana{semana}", figure=fig3, style={"height": "30vh", "margin-right": "10px", "margin-top": "10px"},
                    config = {'toImageButtonOptions': {'format': 'png', 'filename': 'grafico-taxa-engajamento', 'height': 1080, 'width': 1920, 'scale': 1}}),
        ], sm=6),
        dbc.Col([
            dcc.Graph(id = f"grafico-vmg-semana{semana}", figure=fig4, style={"height": "30vh", "margin-top": "10px"},
                    config = {'toImageButtonOptions': {'format': 'png', 'filename': 'grafico-vmg', 'height': 1080, 'width': 1920, 'scale': 1}}),
        ], sm=6),
    ], className="g-0"),
    ])

    return elemento

def criar_post_cards(df, semana):

    posts_cards = []

    for idx, linha in df.iterrows():

        nome = linha["Nome"]
        legenda = linha["Legenda"]
        likes = formatar_numero(int(linha["Likes"]))
        comentarios = formatar_numero(int(linha["Comentarios"]))
        impressoes = formatar_numero(int(linha["Impressoes"]))
        views = formatar_numero(int(linha["Visualizacoes"]))
        engajamento = formatar_numero(int(linha["Engajamento"]))
        compartilhamentos = formatar_numero(int(linha["Compartilhamentos"]))
        link = linha["Link"]
        imagem = f"assets/posts/{nome}-tp{idx+1}-semana{semana}.png"

        plataforma = linha["Plataforma"]

        
        if plataforma == "Instagram":

            card_insta = html.Div(
                dbc.Container(
                    [                        
                        html.Div([
                            html.I(className="bi bi-instagram", 
                                    style={
                                        "font-size": "50px", 
                                        "color": "#80529e",
                                        "position": "absolute",  # Posicionamento absoluto
                                        "top": "10px",  # Alinha no topo com um pequeno espaçamento
                                        "right": "10px",  # Alinha à direita com um pequeno espaçamento
                                        # "text-shadow": "1px 1px 0 #fff, -1px 1px 0 #fff, 1px -1px 0 #fff, -1px -1px 0 #fff",
                                        "z-index": "1"
                                    }), 
                            html.P(legenda, className="lead", 
                                style={
                                    "font-size": "0.9vw",  # Tamanho fixo da fonte do P
                                    "width": "200px",  # Largura fixa
                                    "height": "80px",  # Altura fixa
                                    # "overflow": "hidden",  # Evita que o texto saia dos limites
                                    "z-index": "1",  # Texto abaixo da imagem
                                    "position": "relative",  # Permite sobreposição
                                    "color": "#A8A800",
                                    "padding": "5px",
                                    "text-shadow": "-1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000"
                                }),
                            html.Img(src=f"assets/posts/{nome}-tp{idx+1}-semana{semana}.png",
                                    style={
                                        "position": "absolute",  # Sobreposição
                                        "top": "0",  # Posiciona no topo do contêiner pai
                                        "left": "0",  # Alinha à esquerda
                                        "width": "100%",  # Largura total do contêiner
                                        "height": "100%",  # Altura total do contêiner
                                        "opacity": "0.9",  # Definição da opacidade da imagem
                                        "z-index": "0"  # Imagem atrás do texto
                                    })
                        ], style={
                            "position": "relative",  # Define o contêiner como relativo para a sobreposição funcionar
                            "height": "250px",  # Altura total do bloco de conteúdo
                            "width": "100%",  # Largura total do bloco de conteúdo
                            "overflow": "hidden",  # Garante que os elementos fiquem dentro do contêiner
                            "display": "flex",  # Define layout flexível
                            "flex-direction": "column",  # Alinha itens na vertical
                            "justify-content": "flex-end"  # Alinha o conteúdo ao final
                        }),
                        html.Hr(className="my-2"),
                        dbc.Row([
                            dbc.Col(f"❤️ {likes}", id=f"likes-{idx+1}-semana{semana}", style={"margin-left": "15px", "font-size": "1.1vw"}),
                            dbc.Col(f"💬 {comentarios}", id=f"comentarios-{idx+1}-semana{semana}", style={"margin-right": "15px", "font-size": "1.1vw"}),
                        ], style={"margin-top": "10px"}),
                        dbc.Row([
                            dbc.Col(f"📈 {impressoes}", id=f"impressoes-{idx+1}-semana{semana}", style={"margin-left": "15px", "font-size": "1.1vw"}),
                            dbc.Col(f"👍 {engajamento}", id=f"engajamento-{idx+1}-semana{semana}", style={"margin-right": "15px", "font-size": "1.1vw"}),
                        ], style={"margin-top": "10px"}),
                        html.Hr(className="my-2"),
                        html.P(dbc.Button("Link", color="primary", outline=True, href=link, style={"margin-top": "15px"}), className="d-grid gap-2"),
                    ],
                    fluid=True, 
                    style={"height": "55vh"}
                ),
                className="p-2 bg-body-primary rounded-3",
                style={"border": "2px solid", "border-color": "var(--bs-primary)"}
            )

            posts_cards.append(card_insta)

        elif plataforma == "TikTok":
        
            card_tiktok = html.Div(
                dbc.Container(
                    [
                        html.Div([
                            html.I(className="bi bi-tiktok", 
                                    style={
                                        "font-size": "50px", 
                                        "color": "#d1c39b",
                                        "position": "absolute",  # Posicionamento absoluto
                                        "top": "10px",  # Alinha no topo com um pequeno espaçamento
                                        "right": "10px",  # Alinha à direita com um pequeno espaçamento
                                        # "text-shadow": "1px 1px 0 #fff, -1px 1px 0 #fff, 1px -1px 0 #fff, -1px -1px 0 #fff" 
                                        "z-index": "1"
                                    }),                            
                            html.P(legenda, className="lead", 
                                style={
                                    "font-size": "0.9vw",  # Tamanho fixo da fonte do P
                                    "width": "200px",  # Largura fixa
                                    "height": "80px",  # Altura fixa
                                    # "overflow": "hidden",  # Evita que o texto saia dos limites
                                    "z-index": "1",  # Texto abaixo da imagem
                                    "position": "relative",  # Permite sobreposição
                                    "color": "#A8A800",
                                    "padding": "5px",
                                    "text-shadow": "-1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000"
                                }),
                            html.Img(src=f"assets/posts/{nome}-tp{idx+1}-semana{semana}.png",
                                    style={
                                        "position": "absolute",  # Sobreposição
                                        "top": "0",  # Posiciona no topo do contêiner pai
                                        "left": "0",  # Alinha à esquerda
                                        "width": "100%",  # Largura total do contêiner
                                        "height": "100%",  # Altura total do contêiner
                                        "opacity": "0.9",  # Definição da opacidade da imagem
                                        "z-index": "0"  # Imagem atrás do texto
                                    })
                        ], style={
                            "position": "relative",  # Define o contêiner como relativo para a sobreposição funcionar
                            "height": "250px",  # Altura total do bloco de conteúdo
                            "width": "100%",  # Largura total do bloco de conteúdo
                            "overflow": "hidden",  # Garante que os elementos fiquem dentro do contêiner
                            "display": "flex",  # Define layout flexível
                            "flex-direction": "column",  # Alinha itens na vertical
                            "justify-content": "flex-end"  # Alinha o conteúdo ao final
                        }),
                        html.Hr(className="my-2"),
                        dbc.Row([
                            dbc.Col(f"❤️ {likes}", id=f"likes-{idx+1}-semana{semana}", style={"margin-left": "15px", "font-size": "1.1vw"}),
                            dbc.Col(f"💬 {comentarios}", id=f"comentarios-{idx+1}-semana{semana}", style={"margin-right": "15px", "font-size": "1.1vw"}),
                        ], style={"margin-top": "10px"}),
                        dbc.Row([
                            dbc.Col(f"👍 {engajamento}", id=f"engajamento-{idx+1}-semana{semana}", style={"margin-left": "15px", "font-size": "1.1vw"}),
                            dbc.Col(f"🔀 {compartilhamentos}", id=f"compartilhamentos-{idx+1}-semana{semana}", style={"margin-right": "15px", "font-size": "1.1vw"}),
                        ], style={"margin-top": "10px"}),
                        dbc.Row([
                            dbc.Col(f"👁️ {views}", id=f"views-{idx+1}-semana{semana}", style={"margin-left": "15px", "font-size": "1.1vw"}),
                        ], style={"margin-top": "10px", "margin-bottom": "10px"}),
                        html.Hr(className="my-2"),
                        html.P(dbc.Button("Link", color="primary", outline=True, href=link, style={"margin-top": "15px"}), className="d-grid gap-2"),
                    ],
                    fluid=True, style={"height": "55vh"}
                ),
                className="p-2 bg-body-primary rounded-3",
                style={"border": "2px solid", "border-color": "var(--bs-primary)"}
            )

            posts_cards.append(card_tiktok)

        elif plataforma == "Twitter":

            card_x = html.Div(
                dbc.Container(
                    [
                        html.Div([
                            html.I(className="bi bi-twitter", 
                                    style={
                                        "font-size": "50px", 
                                        "color": "#1DA1F2",
                                        "position": "absolute",  # Posicionamento absoluto
                                        "top": "10px",  # Alinha no topo com um pequeno espaçamento
                                        "right": "10px",  # Alinha à direita com um pequeno espaçamento
                                        # "text-shadow": "1px 1px 0 #fff, -1px 1px 0 #fff, 1px -1px 0 #fff, -1px -1px 0 #fff" 
                                        "z-index": "1"
                                    }), #                             
                            html.P(legenda, className="lead", 
                                style={
                                    "font-size": "0.9vw",  # Tamanho fixo da fonte do P
                                    "width": "200px",  # Largura fixa
                                    "height": "80px",  # Altura fixa
                                    # "overflow": "hidden",  # Evita que o texto saia dos limites
                                    "z-index": "1",  # Texto abaixo da imagem
                                    "position": "relative",  # Permite sobreposição
                                    "color": "#A8A800",
                                    "padding": "5px",
                                    "text-shadow": "-1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000"
                                }),
                            html.Img(src=imagem,
                                    style={
                                        "position": "absolute",  # Sobreposição
                                        "top": "0",  # Posiciona no topo do contêiner pai
                                        "left": "0",  # Alinha à esquerda
                                        "width": "100%",  # Largura total do contêiner
                                        "height": "100%",  # Altura total do contêiner
                                        "opacity": "0.9",  # Definição da opacidade da imagem
                                        "z-index": "0"  # Imagem atrás do texto
                                    })
                        ], style={
                            "position": "relative",  # Define o contêiner como relativo para a sobreposição funcionar
                            "height": "250px",  # Altura total do bloco de conteúdo
                            "width": "100%",  # Largura total do bloco de conteúdo
                            "overflow": "hidden",  # Garante que os elementos fiquem dentro do contêiner
                            "display": "flex",  # Define layout flexível
                            "flex-direction": "column",  # Alinha itens na vertical
                            "justify-content": "flex-end"  # Alinha o conteúdo ao final
                        }),
                        html.Hr(className="my-2"),
                        dbc.Row([
                            dbc.Col(f"❤️ {likes}", id=f"likes-{idx+1}-semana{semana}", style={"margin-left": "15px", "font-size": "1.1vw"}),
                            dbc.Col(f"👍 {engajamento}", id=f"engajamento-{idx+1}-semana{semana}", style={"margin-right": "15px", "font-size": "1.1vw"}),
                        ], style={"margin-top": "10px"}),
                        dbc.Row([
                            dbc.Col(f"📈 {impressoes}", id=f"impressoes-{idx+1}-semana{semana}", style={"margin-left": "15px", "font-size": "1.1vw"}),
                            dbc.Col(f"🔀 {compartilhamentos}", id=f"compartilhamentos-{idx+1}-semana{semana}", style={"margin-right": "15px", "font-size": "1.1vw"}),
                        ], style={"margin-top": "10px", "margin-bottom": "10px"}),
                        html.Hr(className="my-2"),
                        html.P(dbc.Button("Link", color="primary", outline=True, href=link, style={"margin-top": "15px"}), className="d-grid gap-2"),
                    ],
                    fluid=True, 
                    style={"height": "55vh"}
                ),
                className="p-2 bg-body-primary rounded-3",
                style={"border": "2px solid", "border-color": "var(--bs-primary)"}
            )

            posts_cards.append(card_x)

        else:

            card_youtube = html.Div(
                dbc.Container(
                    [
                        html.Div([
                            html.I(className="bi bi-youtube", 
                                    style={
                                        "font-size": "50px", 
                                        "color": "#ad0202",
                                        "position": "absolute",  # Posicionamento absoluto
                                        "top": "10px",  # Alinha no topo com um pequeno espaçamento
                                        "right": "10px",  # Alinha à direita com um pequeno espaçamento
                                        # "text-shadow": "1px 1px 0 #fff, -1px 1px 0 #fff, 1px -1px 0 #fff, -1px -1px 0 #fff" 
                                        "z-index": "1"
                                    }),
                            html.P(legenda, className="lead", 
                                style={
                                    "font-size": "0.9vw",  # Tamanho fixo da fonte do P
                                    "width": "200px",  # Largura fixa
                                    "height": "80px",  # Altura fixa
                                    # "overflow": "hidden",  # Evita que o texto saia dos limites
                                    "z-index": "1",  # Texto abaixo da imagem
                                    "position": "relative",  # Permite sobreposição
                                    "color": "#A8A800",
                                    "padding": "5px",
                                    "text-shadow": "-1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000"
                                }),
                            html.Img(src=imagem,
                                    style={
                                        "position": "absolute",  # Sobreposição
                                        "top": "0",  # Posiciona no topo do contêiner pai
                                        "left": "0",  # Alinha à esquerda
                                        "width": "100%",  # Largura total do contêiner
                                        "height": "100%",  # Altura total do contêiner
                                        "opacity": "0.9",  # Definição da opacidade da imagem
                                        "z-index": "0"  # Imagem atrás do texto
                                    })
                        ], style={
                            "position": "relative",  # Define o contêiner como relativo para a sobreposição funcionar
                            "height": "250px",  # Altura total do bloco de conteúdo
                            "width": "100%",  # Largura total do bloco de conteúdo
                            "overflow": "hidden",  # Garante que os elementos fiquem dentro do contêiner
                            "display": "flex",  # Define layout flexível
                            "flex-direction": "column",  # Alinha itens na vertical
                            "justify-content": "flex-end"  # Alinha o conteúdo ao final
                        }),
                        html.Hr(className="my-2"),
                        dbc.Row([
                            dbc.Col(f"❤️ {likes}", id=f"likes-{idx+1}-semana{semana}", style={"margin-left": "15px", "font-size": "1.1vw"}),
                            dbc.Col(f"💬 {comentarios}", id=f"comentarios-{idx+1}-semana{semana}", style={"margin-right": "15px", "font-size": "1.1vw"}),
                        ], style={"margin-top": "10px"}),
                        dbc.Row([
                            dbc.Col(f"👁️ {views}", id=f"views-{idx+1}-semana{semana}", style={"margin-left": "15px", "font-size": "1.1vw"}),
                            dbc.Col(f"👍 {engajamento}", id=f"engajamento-{idx+1}-semana{semana}", style={"margin-right": "15px", "font-size": "1.1vw"}),
                        ], style={"margin-top": "10px", "margin-bottom": "10px"}),
                        html.Hr(className="my-2"),
                        html.P(dbc.Button("Link", color="primary", outline=True, href=link, style={"margin-top": "15px"}), className="d-grid gap-2"),
                    ],
                    fluid=True, 
                    style={"height": "55vh"}
                ),
                className="p-2 bg-body-primary rounded-3",
                style={"border": "2px solid", "border-color": "var(--bs-primary)"}
            )

            posts_cards.append(card_youtube)
            
    return posts_cards

def criar_tooltips(semana):

    tooltips = []

    for i in range(1, 4):

        likes = dbc.Tooltip("Likes", target=f"likes-{i}-semana{semana}", placement="top")
        comentarios = dbc.Tooltip("Comentarios", target=f"comentarios-{i}-semana{semana}", placement="top")
        impressoes = dbc.Tooltip("Impressões: Número de vezes que o público visualizou a publicação.", target=f"impressoes-{i}-semana{semana}", placement="top")
        visualizacoes = dbc.Tooltip("Visualizações: Número de vezes que o público visualizou a publicação de vídeo.", target=f"views-{i}-semana{semana}", placement="top")
        engajamento = dbc.Tooltip("Engajamento: Número de vezes que o público engajou com a publicação curtindo, comentando ou compartilhando.", target=f"engajamento-{i}-semana{semana}", placement="top")
        compartilhamentos = dbc.Tooltip("Compartilhamentos", target=f"compartilhamentos-{i}-semana{semana}", placement="top")
        
        tooltips.append(likes)
        tooltips.append(comentarios)
        tooltips.append(impressoes)
        tooltips.append(visualizacoes)
        tooltips.append(engajamento)
        tooltips.append(compartilhamentos)

    return tooltips

def layout_cards_semanais(df, semana):

    try:
        card1, card2, card3 = criar_post_cards(df, semana)
        elemento = html.Div([
            dbc.Row([
                dbc.Col([card1], sm=3, width={"offset": 1}),
                dbc.Col([card2], sm=3, style={"margin-left": "20px", "margin-right": "20px"}),
                dbc.Col([card3], sm=3),
            ]),
        ])
    except:
        card1, card2 = criar_post_cards(df, semana)
        elemento = html.Div([
            dbc.Row([
                dbc.Col([card1], sm=3, width={"offset": 2}),
                dbc.Col([card2], sm=3, style={"margin-left": "20px", "margin-right": "20px"}),
            ]),
        ])

    return elemento

